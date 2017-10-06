import feedparser
from pymongo import MongoClient
import pymongo
from flask import Flask
from flask import jsonify
import schedule

app = Flask(__name__)
# Function grabs the rss feed headlines (titles) and returns them as a list
client = MongoClient()
db = client.bbc
bbccollections = db.allcategorise


@app.route('/')
def root():
  return jsonify({'Name':'Raj'})

def storedata(k,url):
        print(k,url)
        feeds = feedparser.parse(url)
        for feed in feeds.entries:
                newsdata = dict()
                newsdata['title'] = str(feed.title)
                newsdata['link'] = str(feed.link)
                newsdata['publish'] = feed.published
                newsdata['category'] = k
                bbccollections.insert_one(newsdata).inserted_id


def read_data(cat):
    data = []
    cur = bbccollections.find({"category": cat}).sort([['publish', pymongo.ASCENDING]])
    for doc in cur:
        data.append({'title': doc['title'], 'link': doc['link'], 'date': doc['publish']})
    return data


# List of RSS feeds that we will fetch and combine
newsurls = {
            1: 'http://feeds.bbci.co.uk/news/world/rss.xml',
            2: 'http://feeds.bbci.co.uk/news/uk/rss.xml',
            3: 'http://feeds.bbci.co.uk/news/business/rss.xml',
            4: 'http://feeds.bbci.co.uk/news/politics/rss.xml',
            5: 'http://feeds.bbci.co.uk/news/health/rss.xml',
            6: 'http://feeds.bbci.co.uk/news/education/rss.xml',
            7: 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
            8: 'http://feeds.bbci.co.uk/news/technology/rss.xml',
            9: 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml'
}
#def update():
#for key, url in newsurls.items():
        #storedata(key,url)
# #schedule.every(10).se.do(update)



# Iterate over the feed urls
@app.route('/rssbbc', methods=['GET'])
def getrssBbc():
    return jsonify({'error massage': 'invalid URL with parameter'})

@app.route('/rssbbc/<category>', methods=['GET'])
def getrssBBCCategories(category):


    if category =='world':
        return jsonify({'result': read_data(1)})
    elif category =='uk':
        return jsonify({'result': read_data(2)})
    elif category =='business':
        return jsonify({'result': read_data(3)})
    elif category =='politics':
        return jsonify({'result': read_data(4)})
    elif category =='health':
        return jsonify({'result': read_data(5)})
    elif category =='education':
        return jsonify({'result': read_data(6)})
    elif category =='scienceandenvironment':
        return jsonify({'result': read_data(7)})
    elif category =='technology':
        return jsonify({'result': read_data(8)})
    elif category =='entertainmentandarts':
        return jsonify({'result': read_data(9)})
    else:
        li = ['world', 'uk', 'business', 'entertainmentandarts', 'politics', 'health', 'education','scienceandenvironment', 'technology' ]
        return jsonify({'message': 'No Category found'}, {'you can choose the Category': li})

if __name__ == '__main__':
    app.run(debug=True)


