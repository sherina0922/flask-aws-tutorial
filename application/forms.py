from flask.ext.wtf import Form
from wtforms import TextField, validators

class EnterDBInfo(Form):
    dbInfo = TextField(label='Items to add to DB', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])

class RetrieveDBInfo(Form):
    userRetrieve = TextField(label='Username of user info to get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter the username of the desired user\'s information')])

class DeleteDBInfo(Form):
    userRetrieve = TextField(label='Username of user to delete from system', description="db_delete", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user who\'s information to delete')])

class UpdateDBInfo(Form):
    userRetrieve = TextField(label='Username of user to update information', description="db_update", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user who\'s information to update and update field: new value')])
