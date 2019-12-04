'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS
Author: Scott Rodkey - rodkeyscott@gmail.com
Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from application import db
from application.models import User, RecommendedRecipe
from application.forms import EnterUserInfo, RetrieveUserInfo, DeleteUserInfo, UpdateUserCalories, EnterRecRecipeInfo, RetrieveRecRecipeInfo, DeleteRecRecipeInfo, UpdateRecRecipeDate, EnterRecipeInfo, GetRecRecipe
from pymongo import MongoClient
import scrape_schema_recipe
import json
from bson import ObjectId
from pandas.io.json import json_normalize
import numpy as np
import re
import datetime
import random

date = 10
# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

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
            (2) recipe MongoDB
    Output: (1) list of data to be stored in MongoDB
    '''

    #Parse url string to locate recipe name and number

    mongo_update_lst = []
    for recipe_url in list_link:
        r = None
        try:
            r = scrape_schema_recipe.scrape_url(recipe_url, python_objects=True)
        except:
            print('Could not scrape URL {}'.format(recipe_url))
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

@application.route('/new', methods=['GET', 'POST'])
@application.route('/new_index', methods=['GET', 'POST'])
def new_index():
    createUserForm = EnterUserInfo(request.form)
    getUserInfoForm = RetrieveUserInfo(request.form)
    deleteUserForm = DeleteUserInfo(request.form)
    updateUserCaloriesForm = UpdateUserCalories(request.form)
    createRecipeForm = EnterRecRecipeInfo(request.form)
    getUserRecRecipeHistForm = RetrieveRecRecipeInfo(request.form)
    deleteUserRecHistForm = DeleteRecRecipeInfo(request.form)
    updateUserRecDateForm = UpdateRecRecipeDate(request.form)
    enterRecipeForm = EnterRecipeInfo(request.form)

    if request.method == 'POST' and createUserForm.validate():
        #userInfoDict = dict(item.split("=") for item in createUserForm.dbInfo.data.split(";"))
        data_entered = User(username=createUserForm.username.data, password=createUserForm.password.data, name=createUserForm.name.data, gender=createUserForm.gender.data, budget=createUserForm.budget.data, calories=createUserForm.calories.data, avg_cals_burned=createUserForm.avgCalBurned.data, location=createUserForm.location.data)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.expunge(query_db)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html',username = createUserForm.username.data,
        password=createUserForm.password.data, name=createUserForm.name.data,
        gender=createUserForm.gender.data, budget=createUserForm.budget.data,
        calories=createUserForm.calories.data,
        avg_cals_burned=createUserForm.avgCalBurned.data,
        location=createUserForm.location.data)
        #change this html

    if request.method == 'POST' and getUserInfoForm.validate():
        query_db = None
        try:
            username_return = getUserInfoForm.userRetrieve.data
            query_db = User.query.filter_by(username=username_return).one()
            db.session.expunge(query_db)
            db.session.close()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('results.html', results=query_db, username_return=username_return)

    # return redirect('/new')
    return render_template('new_index.html', createUserForm=createUserForm,
    getUserInfoForm=getUserInfoForm,deleteUserForm=deleteUserForm,
    updateUserCaloriesForm=updateUserCaloriesForm,createRecipeForm = createRecipeForm,
    getUserRecRecipeHistForm = getUserRecRecipeHistForm, deleteUserRecHistForm = deleteUserRecHistForm,
    updateUserRecDateForm = updateUserRecDateForm, enterRecipeForm=EnterRecipeInfo(request.form))

@application.route('/unregister', methods=['POST'])
def delete_user():
    deleteUserForm = DeleteUserInfo(request.form)
    if request.method == 'POST' and deleteUserForm.validate():
        username_return = deleteUserForm.userRetrieve.data
        try:
            with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("DELETE FROM users WHERE username=(?)",[username_return])
                con.commit()
                cur.close()
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('goodbye.html', username_return=username_return)

@application.route('/update', methods=['GET', 'POST'])
def update_user_calories():
    updateUserCaloriesForm = UpdateUserCalories(request.form)
    if request.method == 'POST' and updateUserCaloriesForm.validate():
        try:
            # userInfoDict = dict(item.split("=") for item in updateUserCaloriesForm.userInfo.data.split(";"))
            # query_db = User.query.filter_by(username=userInfoDict.get("username")).one()
            # query_db.weight = userInfoDict.get("weight")
            query_db = User.query.filter_by(username=updateUserCaloriesForm.username.data).one()
            query_db.calories = updateUserCaloriesForm.newCalories.data
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return redirect('/')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@application.route('/add-history', methods=['GET', 'POST'])
def add_history():
    createRecipeForm = EnterRecRecipeInfo(request.form)
    if request.method == 'POST' and createRecipeForm.validate():
        # userInfoDict = dict(item.split("=") for item in createRecipeForm.dbInfo.data.split(";"))
        data_entered = RecommendedRecipe(user_id=createRecipeForm.username.data, recipe_id=createRecipeForm.recipeId.data, recipe_name=createRecipeForm.recipeName.data, date_recommended=createRecipeForm.date.data)
        try:
            with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("INSERT INTO recommendedrecipes VALUES ((?), (?), (?), (?))", (createRecipeForm.recipeId, createRecipeForm.username.data, createRecipeForm.recipeName.data, createRecipeForm.date.data))
                # result_arr = []
                # for item in query_db:
                #     recipe_dict = {}
                #     recipe_dict["user_id"] = item[0]
                #     recipe_dict["recipe_id"] = item[1]
                #     recipe_dict["recipe_name"] = item[2]
                #     recipe_dict["date_recommended"] = item[3]
                #     result_arr.append(user_dict)
            db.session.add(data_entered)
            db.session.commit()
            db.session.expunge(query_db)
            db.session.close()
        except sqlite3.IntegrityError:
            db.session.rollback()
            return render_template('recipe-insert-fail.html', user_id=createRecipeForm.userId.data, recipe_id=createRecipeForm.recipeId.data)
        except:
            db.session.rollback()
        return render_template('recipe-results.html', results=data_entered)

@application.route('/view-history', methods=['GET', 'POST'])
def view_history():
    getUserRecRecipeHistForm = RetrieveRecRecipeInfo(request.form)
    if request.method == 'POST' and getUserRecRecipeHistForm.validate():
        query_db = None
        try:
            username_return = getUserRecRecipeHistForm.userRetrieve.data
            with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("SELECT * FROM recommendedrecipes WHERE user_id=(?)",[username_return])
                result_arr = []
                for item in query_db:
                    user_dict = {}
                    user_dict["recipe_id"] = item[0]
                    user_dict["user_id"] = item[1]
                    user_dict["recipe_name"] = item[3]
                    user_dict["date_recommended"] = item[2]
                    result_arr.append(user_dict)
            db.session.close()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('view-user-history.html', username_return=username_return, results=result_arr)

@application.route('/delete-history', methods=['POST'])
def delete_history():
    deleteUserRecHistForm = DeleteRecRecipeInfo(request.form)
    if request.method == 'POST' and deleteUserRecHistForm.validate():
        username_return = deleteUserRecHistForm.userRetrieve.data
        try:
            with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("DELETE FROM recommendedrecipes WHERE user_id=(?)", [username_return])
                con.commit()
                cur.close()
            #db.session.commit()
            db.session.close()
            #con.close()
        except:
            db.session.rollback()
        return redirect('/')

@application.route('/update-history', methods=['GET', 'POST'])
def update_user_history():
    updateUserRecDateForm = UpdateRecRecipeDate(request.form)
    if request.method == 'POST' and updateUserRecDateForm.validate():
        userInfoDict = dict(item.split("=") for item in updateUserRecDateForm.userInfo.data.split(";"))
        try:
            with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("UPDATE recommendedrecipes SET date_recommended=(?) WHERE user_id=(?) AND recipe_id=(?)",(userInfoDict.get("date"), userInfoDict.get("username"), userInfoDict.get("recipe_id")))
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return redirect('/')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@application.route('/list_recipes', methods=['GET', 'POST'])
def get_recipes():
    recipes_list = read_mongo(recipe_db)
    return JSONEncoder().encode(recipes_list)

def join_user_recipes(user_id):
    rec_recipes_dict = []
    with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
        cur = con.cursor()
        query_db = cur.execute("SELECT recommendedrecipes.recipe_id, recommendedrecipes.date_recommended FROM users JOIN recommendedrecipes ON users.username = recommendedrecipes.user_id WHERE users.username=((?))", [user_id])
        for item in query_db:
            new_item = {}
            new_item["recipe_id"] = item[0]
            new_item["date_recommended"] = item[1]
            print("item:", item[0],item[1])
            rec_recipes_dict.append(new_item)
        db.session.close()
    return rec_recipes_dict


def recommend_recipes(user_data):
    all_recipes = read_mongo(recipe_db)
    random.shuffle(all_recipes)
    recipe_list = []
    total_cals = 0
    total_recipes = 0
    global date
    #check the budget
    for recipe in all_recipes:
        if total_recipes > 5:
            break
        recipe_data = get_recipe_info(recipe)
        if not recipe_data['calories']:
            continue
        recipe_cals = recipe_data['calories'].split()
        if (total_cals + int(recipe_cals[0])) <= (user_data["calories"] + user_data["avg_cals_burned"]):
            try:
                past_recipes_dict = join_user_recipes(user_data["username"])
                with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                    cur = con.cursor()
                    for past_recipes in past_recipes_dict:
                        if str(recipe["_id"]) == past_recipes["recipe_id"]:
                            past_date = datetime.datetime.strptime(past_recipes["date_recommended"], "%m/%d/%Y").date()
                            new_date = datetime.datetime.strptime("12/" + str(date) + "/2019", "%m/%d/%Y").date()
                            elapsed_days = divmod((new_date-past_date).total_seconds(), 86400)[0]
                            if abs(elapsed_days) > 2:
                                query_db = cur.execute("DELETE FROM recommendedrecipes WHERE recipe_id=(?)",[str(recipe["_id"])])
                                db.session.commit()
                            break
                    query_db = cur.execute("INSERT INTO recommendedrecipes VALUES ((?), (?), (?), (?))", (str(recipe["_id"]), user_data["username"], recipe["name"], "12/" + str(date) + "/2019"))
                    db.session.commit()
                    db.session.close()
                    recipe_list.append(recipe_data)
                    total_cals += int(recipe_cals[0])
                    total_recipes += 1
            except sqlite3.IntegrityError: #to check that the same recipe is not being recommened again
                continue
    # return jsonify({'recipes': recipe_list})
    # df = json_normalize({'recipes': recipe_list})
    # parsed = json.loads({'recipes': recipe_list})
    # return pandas.read_json(parsed)
    date += 1 #for testing and demo purposes
    return jsonify({'recipes': recipe_list})
    # return json.dumps(parsed, indent=2, sort_keys=True)
    # return np.var(df.values)


def get_recipe_info(recipe):
    try:
        name = recipe['name']
    except AttributeError:
        name = None

    try:
        ingredients = recipe['recipeIngredient']
    except AttributeError:
        ingredients = None

    try:
        instructions = recipe['recipeInstructions']
    except AttributeError:
        instructions = None

    # try:
    #     author = recipe['author']
    # except AttributeError:
    #     author = None

    try:
        prepTime = recipe['prepTime']
    except KeyError:
        prepTime = None

    try:
        calories = recipe['nutrition']['properties']['calories']
    except KeyError:
        calories = recipe['nutrition']['calories']
    except:
        calories = None

    return {
        'name': name,
        'ingredients': ingredients,
        'instructions': instructions,
        'prepTime': prepTime,
        'calories': calories,
    }

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    createUserForm = EnterUserInfo(request.form)
    getUserInfoForm = RetrieveUserInfo(request.form)
    deleteUserForm = DeleteUserInfo(request.form)
    updateUserCaloriesForm = UpdateUserCalories(request.form)
    createRecipeForm = EnterRecRecipeInfo(request.form)
    getUserRecRecipeHistForm = RetrieveRecRecipeInfo(request.form)
    deleteUserRecHistForm = DeleteRecRecipeInfo(request.form)
    updateUserRecDateForm = UpdateRecRecipeDate(request.form)
    enterRecipeForm = EnterRecipeInfo(request.form)

    if request.method == 'POST' and createUserForm.validate():
        #userInfoDict = dict(item.split("=") for item in createUserForm.dbInfo.data.split(";"))
        data_entered = User(username=createUserForm.username.data, password=createUserForm.password.data, name=createUserForm.name.data, gender=createUserForm.gender.data, budget=createUserForm.budget.data, calories=createUserForm.calories.data, avg_cals_burned=createUserForm.avgCalBurned.data, location=createUserForm.location.data)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.expunge(query_db)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html',username = createUserForm.username.data,
        password=createUserForm.password.data, name=createUserForm.name.data,
        gender=createUserForm.gender.data, budget=createUserForm.budget.data,
        calories=createUserForm.calories.data,
        avg_cals_burned=createUserForm.avgCalBurned.data,
        location=createUserForm.location.data)
        #change this html

    if request.method == 'POST' and getUserInfoForm.validate():
        query_db = None
        try:
            username_return = getUserInfoForm.userRetrieve.data
            query_db = User.query.filter_by(username=username_return).one()
            db.session.expunge(query_db)
            db.session.close()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('results.html', results=query_db, username_return=username_return)

    return render_template('index.html', createUserForm=createUserForm,
    getUserInfoForm=getUserInfoForm,deleteUserForm=deleteUserForm,
    updateUserCaloriesForm=updateUserCaloriesForm,createRecipeForm = createRecipeForm,
    getUserRecRecipeHistForm = getUserRecRecipeHistForm, deleteUserRecHistForm = deleteUserRecHistForm,
    updateUserRecDateForm = updateUserRecDateForm, enterRecipeForm=EnterRecipeInfo(request.form))

@application.route('/get_forms', methods=['GET', 'POST'])
def get_all_forms():
    return redirect('/')

@application.route('/get_recommendations', methods=['GET', 'POST'])
def get_recommendations():
    getRecRecipeForm = GetRecRecipe(request.form)
    return render_template('get_recipes.html', getRecRecipeForm=getRecRecipeForm)

@application.route('/view-recommendations', methods=['GET', 'POST'])
def check_user_for_recommendations():
    getRecRecipeForm = GetRecRecipe(request.form)
    if request.method == 'POST' and getRecRecipeForm.validate():
        result_arr = []
        username_return = getRecRecipeForm.userRetrieve.data
        try:
            with sqlite3.connect("/Users/ritikasinha/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("SELECT * FROM users WHERE username=(?)",[username_return])
                for item in query_db:
                    user_dict = {}
                    user_dict["name"] = item[0]
                    user_dict["username"] = item[1]
                    user_dict["password"] = item[2]
                    user_dict["gender"] = item[3]
                    user_dict["budget"] = item[4]
                    user_dict["calories"] = item[5]
                    user_dict["avg_cals_burned"] = item[6]
                    user_dict["location"] = item[7]
                    result_arr.append(user_dict)
            cur.close()
            db.session.close()
            return recommend_recipes(result_arr[0])
        except:
            db.session.rollback()
        # return redirect('/')
        # print(result_arr)
        # recipes_list = read_mongo(recipe_db)
        # return JSONEncoder().encode(recipes_list)
        return render_template('noresult.html', username_return=username_return)
    # return render_template('get_recipes.html', getRecRecipeForm=getRecRecipeForm)

if __name__ == '__main__':
    # Test for mongo and set up for collection/etc
    f = open("recipes.txt", "r")
    if f.mode == "r":
        contents = f.read()
    #list_links = contents.split(",")
    list_links = ['http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx', 'http://www.epicurious.com/recipes/food/views/chocolate-amaretto-souffles-104730', 'http://www.epicurious.com/recipes/food/views/coffee-almond-ice-cream-cake-with-dark-chocolate-sauce-11036', 'http://www.epicurious.com/recipes/food/views/toasted-almond-mocha-ice-cream-tart-12550']
    db_client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
    db_mongo = db_client.allrecipes
    recipe_db = db_mongo.recipe_data
    mongo_data = scrape_search(list_links)

    x = recipe_db.delete_many({})
    store_data(mongo_data, recipe_db)
    # mongo_retrieve = read_mongo(recipe_db)
    # for recipe in mongo_retrieve:
    #     recipe_data = get_recipe_info(recipe)
    #     print(recipe_data['calories'])
    application.run(host='0.0.0.0')
