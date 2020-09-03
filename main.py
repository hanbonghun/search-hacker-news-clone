import requests
from flask import Flask, render_template,request

import json

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

def make_detail_url(id):
  return f"{base_url}/items/{id}"

def get_comments(id):
    url = make_detail_url(id)
    result = requests.get(url).json()
    result = result['children']
    comments = []
    for i in range(len(result)):  #len(result)
        author = result[i]['author']
        text = result[i]['text']
        if author is None:
            author = ""
            text= "[deleted]"
        temp = {'author':author, 'text':text}
        comments.append(temp)
    return comments

def get_articles(url):
    articles = []
    result = requests.get(url).json()
    result =  result['hits']
    dic = dict()
    for i in range(len(result)):
        title = result[i]['title']
        link = result[i]['url']
        author = result[i]['author']
        points = result[i]['points']
        num_comments = result[i]['num_comments']
        id = result[i]['objectID']
        comments = get_comments(id)
        dic[id] = {'title':title, 'link':link, 'author':author, 'points':points, 'num_comments':num_comments, 'comments':comments}
    return dic

db = {}
db = get_articles(popular)

db2 ={}
db2 = get_articles(new)

app = Flask("DayNine")

@app.route('/')
def home():
    if request.args.get('order_by') == 'popular':
        return render_template('index.html', articles = db ,new =0)
    elif request.args.get('order_by') == 'new':
        return render_template('index.html', articles = db2,new =1)
    else:
        return render_template('index.html', articles = db, new = 0)


@app.route('/<id>')
def aa(id):
    try:
        return render_template('detail.html', article = db[id])
    except:
        return render_template('detail.html', article = db2[id])

app.run()
