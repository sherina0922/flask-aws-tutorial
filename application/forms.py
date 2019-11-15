from flask.ext.wtf import Form
from wtforms import TextField, validators

class EnterUserInfo(Form):
    dbInfo = TextField(label='User to add', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])

class RetrieveUserInfo(Form):
    userRetrieve = TextField(label='Username of user info to get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter the username of the desired user\'s information')])

class DeleteUserInfo(Form):
    userRetrieve = TextField(label='Username of user to delete from system', description="db_delete", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user who\'s information to delete')])

class UpdateUserWeight(Form):
    userInfo = TextField(label='Username of user to update weight', description="db_update", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user who\'s information to update and update field: new value')])

class EnterRecRecipeInfo(Form):
    dbInfo = TextField(label='Receipt of recommended recipe to add', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])

class RetrieveRecRecipeInfo(Form):
    userRetrieve = TextField(label='Find all recommended recipes of user', description="db_get", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter the username of the desired user')])

class DeleteRecRecipeInfo(Form):
    userRetrieve = TextField(label='Delete recommended recipe history for given user', description="db_delete", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the user id to clear recommendation history')])

class UpdateRecRecipeDate(Form):
    userInfo = TextField(label='Username and recipe id to change recipe date', description="db_update", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user and the recipe id to update and update date recommended')])

class EnterTaskInfo(Form):
    taskInfo = TextField(label='Title and description of the task', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the title and description of task')])
