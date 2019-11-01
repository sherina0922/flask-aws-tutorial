from flask.ext.wtf import Form
from wtforms import TextField, validators

class EnterDBInfo(Form):
    dbInfo = TextField(label='Items to add to DB', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])

class RetrieveDBInfo(Form):
    userRetrieve = TextField(label='Username of user info to get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=256, message=u'Enter the username of the desired user\'s information')])
