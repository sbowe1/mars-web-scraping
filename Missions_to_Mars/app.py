from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create flask app
app = Flask(__name__)

# Establish Mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

# App routes
@app.route('/')
def home():
    mars_data = mongo.db.collection.find_one()

    return render_template('index.html', mars=mars_data)

@app.route('/scrape')
def scraper():
    data = scrape_mars.scrape()

    # Update Mongo database
    mongo.db.collection.update_one({}, {'$set': data}, upsert=True)

    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)