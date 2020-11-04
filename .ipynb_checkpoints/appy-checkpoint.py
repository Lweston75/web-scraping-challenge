  
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:5433/mars_app")



@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()

    
    return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scrape():

    scraped_data = scrape_mars.scrape()

 
    mars_data.update({}, scraped_data, upsert=True)

 
    return redirect("/data")


@app.route("/data")
def data():

    
    mars_info = mongo.db.mars_data.find_one()


    return render_template("data.html", info=mars_info)


if __name__ == "__main__":
    app.run(debug=True)