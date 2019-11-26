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
from application.forms import EnterUserInfo, RetrieveUserInfo, DeleteUserInfo, UpdateUserWeight, EnterRecRecipeInfo, RetrieveRecRecipeInfo, DeleteRecRecipeInfo, UpdateRecRecipeDate, EnterTaskInfo
from pymongo import MongoClient
#import logging
#from sqlachemy.exc import IntegrityError

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
db_mongo = client.mymongodb  # Select the database
tasks_collection = db_mongo.task  # Select the collection name
initial_tasks = [task for task in tasks_collection.find()]
if (len(initial_tasks)) == 0:
    tasks_collection.insert({
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Yeet',
        'done': False
    })
    tasks_collection.insert({
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    })
    tasks_collection.insert({
        'id': 3,
        'title': u'GIVE UP ON 411',
        'description': u'ABDU ALAWINIIIIII',
        'done': False
    })

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    createUserForm = EnterUserInfo(request.form)
    getUserInfoForm = RetrieveUserInfo(request.form)
    deleteUserForm = DeleteUserInfo(request.form)
    updateUserWeightForm = UpdateUserWeight(request.form)
    createRecipeForm = EnterRecRecipeInfo(request.form)
    getUserRecRecipeHistForm = RetrieveRecRecipeInfo(request.form)
    deleteUserRecHistForm = DeleteRecRecipeInfo(request.form)
    updateUserRecDateForm = UpdateRecRecipeDate(request.form)
    enterTaskForm = EnterTaskInfo(request.form)

    if request.method == 'POST' and createUserForm.validate():
        #userInfoDict = dict(item.split("=") for item in createUserForm.dbInfo.data.split(";"))
        data_entered = User(username=createUserForm.username.data, password=createUserForm.password.data, name=createUserForm.name.data, gender=createUserForm.gender.data, budget=createUserForm.budget.data, weight=createUserForm.weight.data, weight_goal=createUserForm.weightGoal.data, avg_cals_burned=createUserForm.avgCalBurned.data, location=createUserForm.location.data, notes=createUserForm.notes.data)
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
        weight=createUserForm.weight.data, weight_goal=createUserForm.weightGoal.data,
        avg_cals_burned=createUserForm.avgCalBurned.data,
        location=createUserForm.location.data, notes=createUserForm.notes.data)
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
    updateUserWeightForm=updateUserWeightForm,createRecipeForm = createRecipeForm,
    getUserRecRecipeHistForm = getUserRecRecipeHistForm, deleteUserRecHistForm = deleteUserRecHistForm,
    updateUserRecDateForm = updateUserRecDateForm, enterTaskForm=EnterTaskInfo(request.form))

@application.route('/unregister', methods=['POST'])
def delete_user():
    deleteUserForm = DeleteUserInfo(request.form)
    if request.method == 'POST' and deleteUserForm.validate():
        username_return = deleteUserForm.userRetrieve.data
        try:
            with sqlite3.connect("/Users/sherinahung/Downloads/flask-aws-tutorial/application/test.db") as con:
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
def update_user_weight():
    updateUserWeightForm = UpdateUserWeight(request.form)
    if request.method == 'POST' and updateUserWeightForm.validate():
        try:
            # userInfoDict = dict(item.split("=") for item in updateUserWeightForm.userInfo.data.split(";"))
            # query_db = User.query.filter_by(username=userInfoDict.get("username")).one()
            # query_db.weight = userInfoDict.get("weight")
            query_db = User.query.filter_by(username=updateUserWeightForm.username.data).one()
            query_db.weight = updateUserWeightForm.newWeight.data
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
            with sqlite3.connect("/Users/sherinahung/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("INSERT INTO recommendedrecipes VALUES ((?), (?), (?), (?))",createRecipeForm.username.data, createRecipeForm,recipeId, createRecipeForm.recipeName.data, createRecipeForm.date.data)
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
            with sqlite3.connect("/Users/sherinahung/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("SELECT * FROM recommendedrecipes WHERE user_id=(?)",[username_return])
                result_arr = []
                for item in query_db:
                    user_dict = {}
                    user_dict["recipe_id"] = item[0]
                    user_dict["user_id"] = item[1]
                    user_dict["recipe_name"] = item[2]
                    user_dict["date_recommended"] = item[3]
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
            with sqlite3.connect("/Users/sherinahung/Downloads/flask-aws-tutorial/application/test.db") as con:
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
            with sqlite3.connect("/Users/sherinahung/Downloads/flask-aws-tutorial/application/test.db") as con:
                cur = con.cursor()
                query_db = cur.execute("UPDATE recommendedrecipes SET date_recommended=(?) WHERE user_id=(?) AND recipe_id=(?)",(userInfoDict.get("date"), userInfoDict.get("username"), userInfoDict.get("recipe_id")))
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return redirect('/')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

@application.route('/list_tasks', methods=['GET', 'POST'])
def get_tasks():
    all_tasks = tasks_collection.find()
    task_list = []
    for task in all_tasks:
        task_list.append({'title': task['title'], 'description': task['description'], 'id': task['id']})

    return jsonify({'tasks': task_list})

@application.route('/add_tasks', methods=['GET', 'POST'])
def create_task():
    enterTaskForm = EnterTaskInfo(request.form)
    if request.method == 'POST' and enterTaskForm.validate():
        tasks = tasks_collection.find()
        taskInfoDict = dict(item.split("=") for item in enterTaskForm.taskInfo.data.split(";"))
        new_task = {"id": tasks.count(), "title": taskInfoDict.get("title"), "description": taskInfoDict.get("description"), "done": False}
        tasks_collection.insert(new_task)
        all_tasks = tasks_collection.find()
        task_list = []
        for task in all_tasks:
            task_list.append({'title': task['title'], 'description': task['description'], 'id': task['id']})
        return jsonify({'tasks': task_list})

@application.route('/new', methods=['GET', 'POST'])
@application.route('/new_index', methods=['GET', 'POST'])
def new_index():
    createUserForm = EnterUserInfo(request.form)
    getUserInfoForm = RetrieveUserInfo(request.form)
    deleteUserForm = DeleteUserInfo(request.form)
    updateUserWeightForm = UpdateUserWeight(request.form)
    createRecipeForm = EnterRecRecipeInfo(request.form)
    getUserRecRecipeHistForm = RetrieveRecRecipeInfo(request.form)
    deleteUserRecHistForm = DeleteRecRecipeInfo(request.form)
    updateUserRecDateForm = UpdateRecRecipeDate(request.form)
    enterTaskForm = EnterTaskInfo(request.form)

    if request.method == 'POST' and createUserForm.validate():
        #userInfoDict = dict(item.split("=") for item in createUserForm.dbInfo.data.split(";"))
        data_entered = User(username=createUserForm.username.data, password=createUserForm.password.data, name=createUserForm.name.data, gender=createUserForm.gender.data, budget=createUserForm.budget.data, weight=createUserForm.weight.data, weight_goal=createUserForm.weightGoal.data, avg_cals_burned=createUserForm.avgCalBurned.data, location=createUserForm.location.data, notes=createUserForm.notes.data)
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
        weight=createUserForm.weight.data, weight_goal=createUserForm.weightGoal.data,
        avg_cals_burned=createUserForm.avgCalBurned.data,
        location=createUserForm.location.data, notes=createUserForm.notes.data)
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

    return render_template('new_index.html', createUserForm=createUserForm,
    getUserInfoForm=getUserInfoForm,deleteUserForm=deleteUserForm,
    updateUserWeightForm=updateUserWeightForm,createRecipeForm = createRecipeForm,
    getUserRecRecipeHistForm = getUserRecRecipeHistForm, deleteUserRecHistForm = deleteUserRecHistForm,
    updateUserRecDateForm = updateUserRecDateForm, enterTaskForm=EnterTaskInfo(request.form))

@application.route('/get_forms', methods=['GET', 'POST'])
def get_all_forms():
    return redirect('/new')

if __name__ == '__main__':
    application.run(host='0.0.0.0')
