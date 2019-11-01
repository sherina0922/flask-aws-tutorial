'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, flash, redirect, url_for
from application import db
from application.models import User, RecommendedRecipe
from application.forms import EnterUserInfo, RetrieveUserInfo, DeleteUserInfo, UpdateUserWeight, EnterRecRecipeInfo, RetrieveRecRecipeInfo, DeleteRecRecipeInfo, UpdateRecRecipeDate
#import logging
#from sqlachemy.exc import IntegrityError

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

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

    if request.method == 'POST' and createUserForm.validate():
        userInfoDict = dict(item.split("=") for item in createUserForm.dbInfo.data.split(";"))
        data_entered = User(username=userInfoDict.get("username"), password=userInfoDict.get("password"), name=userInfoDict.get("name"), gender=userInfoDict.get("gender"), budget=userInfoDict.get("budget"), weight=userInfoDict.get("weight"), weight_goal=userInfoDict.get("weight_goal"), avg_cals_burned=userInfoDict.get("avg_cals_burned"), location=userInfoDict.get("location"), notes=userInfoDict.get("notes"))
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        # except IntegrityError as e:
        #     reason = e.message
        #     logging.warning(reason)
        except:
            db.session.rollback()
        return render_template('thanks.html',username = userInfoDict.get("username"),
        password=userInfoDict.get("password"), name=userInfoDict.get("name"),
        gender=userInfoDict.get("gender"), budget=userInfoDict.get("budget"),
        weight=userInfoDict.get("weight"), weight_goal=userInfoDict.get("weight_goal"),
        avg_cals_burned=userInfoDict.get("avg_cals_burned"),
        location=userInfoDict.get("location"), notes=userInfoDict.get("notes"))
        #change this html

    if request.method == 'POST' and getUserInfoForm.validate():
        query_db = None
        try:
            username_return = getUserInfoForm.userRetrieve.data
            query_db = User.query.filter_by(username=username_return).one()
            db.session.close()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('results.html', results=query_db, username_return=username_return)

    return render_template('index.html', createUserForm=createUserForm,
    getUserInfoForm=getUserInfoForm,deleteUserForm=deleteUserForm,
    updateUserWeightForm=updateUserWeightForm,createRecipeForm = createRecipeForm,
    getUserRecRecipeHistForm = getUserRecRecipeHistForm, deleteUserRecHistForm = deleteUserRecHistForm,
    updateUserRecDateForm = updateUserRecDateForm)

@application.route('/unregister', methods=['POST'])
def delete_user():
    deleteUserForm = DeleteUserInfo(request.form)
    if request.method == 'POST' and deleteUserForm.validate():
        try:
            username_return = deleteUserForm.userRetrieve.data
            query_db = User.query.filter_by(username=username_return).one()
            db.session.delete(query_db)
            db.session.commit()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('goodbye.html', username_return=username_return)

@application.route('/update', methods=['GET', 'POST'])
def update_user_weight():
    updateUserWeightForm = UpdateUserWeight(request.form)
    if request.method == 'POST' and updateUserWeightForm.validate():
        try:
            userInfoDict = dict(item.split("=") for item in updateUserWeightForm.userInfo.data.split(";"))
            query_db = User.query.filter_by(username=userInfoDict.get("username")).one()
            query_db.weight = userInfoDict.get("weight")
            db.session.commit()
        except:
            db.session.rollback()
        return redirect('/')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@application.route('/add-history', methods=['GET', 'POST'])
def add_history():
    createRecipeForm = EnterRecRecipeInfo(request.form)
    if request.method == 'POST' and createRecipeForm.validate():
        userInfoDict = dict(item.split("=") for item in createRecipeForm.dbInfo.data.split(";"))
        data_entered = RecommendedRecipe(user_id=userInfoDict.get("username"), recipe_id=userInfoDict.get("recipe_id"), recipe_name=userInfoDict.get("recipe_name"), date_recommended=userInfoDict.get("date"))
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return redirect('/')# return render_template()

@application.route('/view-history', methods=['GET', 'POST'])
def view_history():
    getUserRecRecipeHistForm = RetrieveRecRecipeInfo(request.form)
    if request.method == 'POST' and getUserRecRecipeHistForm.validate():
        query_db = None
        try:
            username_return = getUserRecRecipeHistForm.userRetrieve.data
            query_db = RecommendedRecipe.query.filter_by(user_id=username_return)
            db.session.close()
        except:
            db.session.rollback()
            return render_template('noresult.html', username_return=username_return)
        return render_template('view-user-history.html', username_return=username_return, results=query_db)


@application.route('/delete-history', methods=['POST'])
def delete_history():
    deleteUserRecHistForm = DeleteRecRecipeInfo(request.form)
    if request.method == 'POST' and deleteUserRecHistForm.validate():
        username_return = deleteUserForm.userRetrieve.data
        # query_db = RecommendedRecipe.query.filter_by(user_id=username_return)
        try:
            # db.session.delete(query_db)
            # RecommendedRecipe.delete().where(user_id=username_return)
            db.session.query(RecommendedRecipe).filter(user_id=username_return).delete(synchronize_session='fetch')
            db.session.commit()
            flash('User recipe history was deleted.')
        except:
            db.session.rollback()
        return redirect('/')

@application.route('/update-history', methods=['GET', 'POST'])
def update_user_history():
    updateUserRecDateForm = UpdateRecRecipeDate(request.form)
    if request.method == 'POST' and updateUserRecDateForm.validate():
        userInfoDict = dict(item.split("=") for item in updateUserWeightForm.userInfo.data.split(";"))
        query_db = RecommendedRecipe.query.filter_by(user_id=userInfoDict.get("username"), recipe_id=userInfoDict.get("recipe_id")).one()
        try:
            query_db.date_recommended = userInfoDict.get("date")
            db.session.commit()
        except:
            db.session.rollback()
        return redirect('/')



if __name__ == '__main__':
    application.run(host='0.0.0.0')
