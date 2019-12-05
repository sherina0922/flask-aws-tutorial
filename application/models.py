from application import db
from pymongo import MongoClient
import scrape_schema_recipe
import datetime
import json
from bson import ObjectId
import csv
import pandas as pd
import sys, getopt, pprint
from pprint import pprint
from sqlalchemy.orm import relationship, backref

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) #change integer to string for username
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(16))
    name = db.Column(db.String(128))
    gender = db.Column(db.String(1))
    budget = db.Column(db.Float)
    calories = db.Column(db.Float)
    avg_cals_burned = db.Column(db.Float)
    location = db.Column(db.String(128))

    def __init__(self, username, password, name, gender, budget, calories, avg_cals_burned, location):
        self.name = name
        self.username = username
        self.password = password
        self.gender = gender
        self.budget = budget
        self.calories = calories
        self.avg_cals_burned = avg_cals_burned
        self.location = location

    def __repr__(self):
        return '<User %r>' % self.name

class RecommendedRecipe(db.Model):
    __tablename__ = 'recommendedrecipes'
    recipe_id = db.Column(db.Integer, primary_key=True) #change integer to string for username
    user_id = db.Column(db.String(128), primary_key=True)
    recipe_name = db.Column(db.String(128))
    date_recommended = db.Column(db.String(128))

    def __init__(self, recipe_id, user_id, recipe_name, date_recommended):
        self.recipe_id = recipe_id
        self.user_id = user_id
        self.date_recommended = date_recommended
        self.recipe_name = recipe_name

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name

class Friends(db.Model):
    __tablename__ = 'friends'
    user_name = db.Column(db.String(128), db.ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    friend_name = db.Column(db.String(128), db.ForeignKey(User.username, ondelete='CASCADE'), primary_key=True) #change integer to string for username

    friend_users = relationship("User", foreign_keys=[user_name], single_parent=True)
    friends = relationship("User", foreign_keys=[friend_name], single_parent=True)


    def __init__(self, friend_name, user_name):
        self.friend_name = friend_name
        self.user_name = user_name

    def __repr__(self):
        return '<Friends %r>' % self.friend_name

#===========================MONGO SET UP==================================

db_client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
db_mongo = db_client.allrecipes
recipe_db = db_mongo.recipe_data
db_mongo_produce = db_client.allproduce
produce_db = db_mongo_produce.produce_data

def RecipeMongoSetUp():
    f = open("recipes.txt", "r")
    if f.mode == "r":
        contents = f.read()
    #list_links = ['http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx', 'http://www.epicurious.com/recipes/food/views/chocolate-amaretto-souffles-104730', 'http://www.epicurious.com/recipes/food/views/coffee-almond-ice-cream-cake-with-dark-chocolate-sauce-11036', 'http://www.epicurious.com/recipes/food/views/toasted-almond-mocha-ice-cream-tart-12550']
    list_links = contents.split(",")
    mongo_data = scrape_search(list_links)
    x = recipe_db.delete_many({})
    store_data(mongo_data, recipe_db)
    mongo_retrieve = read_mongo(recipe_db)
    return mongo_retrieve

def ProduceMongoSetUp():
    csvfile = open('produce_abridged.csv', 'r')
    reader = csv.DictReader(csvfile)
    y = produce_db.delete_many({})
    store_produce(reader, produce_db)
    produce_retrieve = read_mongo_produce(produce_db)
    return produce_retrieve

def store_data(mongo_update_lst, recipe_db):
    '''
    Store Recipe Information in MongoDB
    '''

    for json_dct in mongo_update_lst:
        json_dct = date_hook(json_dct)
        recipe_db.insert_one(json_dct)
    pass

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        if type(value) == datetime.timedelta:
            json_dict[key] = str(value)
    return json_dict

def scrape_search(list_link):
    '''
    Input:  (1) link to search page
    Output: (1) list of data to be stored in MongoDB
    '''

    mongo_update_lst = []
    for recipe_url in list_link:
        r = None
        try:
            r = scrape_schema_recipe.scrape_url(recipe_url, python_objects=True)
        except:
            print('Could not scrape URL {}'.format(recipe_url))
        print(recipe_url)
        mongo_update_lst.append(r[0])
    return mongo_update_lst

def read_mongo(collection, query={}):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    cursor = collection.find()
    recipe_list = []
    for obj in cursor:
        recipe_list.append(obj)

    return recipe_list

def store_produce(reader, produce_db):
    header = ['item_name', 'price']
    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]
        produce_db.insert(row)

def read_mongo_produce(collection, query={}):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    cursor = collection.find()
    produce_list = []
    for obj in cursor:
        produce_list.append(obj)

    return produce_list
