from flask import Flask
from flask import jsonify
from flask import request
import feedparser
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'

mongo = PyMongo(app)

@app.route('/')
def root():
  return jsonify({'Name':'Raj'})


def parseRSS(rss_url):
    return feedparser.parse(rss_url)


@app.route('/rssbbc', methods=['GET'])
def rssbbc():
        headlines = []
        feed = parseRSS('http://feeds.bbci.co.uk/news/world/rss.xml')
        for newsitem in feed['items']:
            headlines.append(newsitem['title'])
        return headlines
        return 'ffffffff'




if __name__ == '__main__':
    app.run(debug=True)
