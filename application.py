'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from application import db
from application.models import User
from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form)
    form2 = RetrieveDBInfo(request.form)

    if request.method == 'POST' and form1.validate():
        userInfoDict = dict(item.split("=") for item in form1.dbInfo.data.split(";"))
        data_entered = User(username=userInfoDict.get("username"), password=userInfoDict.get("password"), name=userInfoDict.get("name"), gender=userInfoDict.get("gender"), budget=userInfoDict.get("budget"), weight=userInfoDict.get("weight"), weight_goal=userInfoDict.get("weight_goal"), avg_cals_burned=userInfoDict.get("avg_cals_burned"), location=userInfoDict.get("location"), notes=userInfoDict.get("notes"))
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html',username = userInfoDict.get("username"), password=userInfoDict.get("password"), name=userInfoDict.get("name"), gender=userInfoDict.get("gender"), budget=userInfoDict.get("budget"), weight=userInfoDict.get("weight"), weight_goal=userInfoDict.get("weight_goal"), avg_cals_burned=userInfoDict.get("avg_cals_burned"), location=userInfoDict.get("location"), notes=userInfoDict.get("notes")) #change this html

    if request.method == 'POST' and form2.validate():
        query_db = None
        username_return = form2.userRetrieve.data
        query_db = User.query.filter_by(username=username_return).one()
        try:
            # user_id_return = form2.userRetrieve.data
            # query_db = Data.query.filter_by(user_id=user_id_return).one()
            db.session.close()
        except:
            username_return = "failed"
            db.session.rollback()
        return render_template('results.html', results=query_db, username_return=username_return)

    return render_template('index.html', form1=form1, form2=form2)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
