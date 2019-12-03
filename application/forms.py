from flask.ext.wtf import Form
from wtforms import TextField, validators, DateField

class EnterUserInfo(Form):
    username = TextField(label='Enter username', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    password = TextField(label='Enter password', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=16, message=u'Enter 16 characters or less')])
    name = TextField(label='Enter first name', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    gender = TextField(label='Enter gender', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1, message=u'Enter 1 character or less')])
    budget = TextField(label='Enter desired budget', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])
    weight = TextField(label='Enter current weight', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])
    weightGoal = TextField(label='Enter desired weight goal', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])
    avgCalBurned = TextField(label='Enter avg calories burned in a day', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter 1024 characters or less')])
    location = TextField(label='Enter current city', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    notes = TextField(label='Enter any additional tidbits', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])

class RetrieveUserInfo(Form):
    userRetrieve = TextField(label='Username of user info to get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter the username of the desired user\'s information')])

class DeleteUserInfo(Form):
    userRetrieve = TextField(label='Username of user to delete from system', description="db_delete", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user who\'s information to delete')])

class UpdateUserWeight(Form):
    username = TextField(label='Username of user to update weight', description="db_update", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter username')])
    newWeight = TextField(label='New weight', description="db_update", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter new current weight')])

class EnterRecRecipeInfo(Form):
    username = TextField(label='Enter username', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    recipeId = TextField(label='Enter recipe id', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=16, message=u'Enter 16 characters or less')])
    recipeName = TextField(label='Enter recipe name', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    date = TextField(label='Enter date (format: mm-dd-yy)', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])

class RetrieveRecRecipeInfo(Form):
    userRetrieve = TextField(label='Find all recommended recipes of user', description="db_get", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter the username of the desired user')])

class DeleteRecRecipeInfo(Form):
    userRetrieve = TextField(label='Delete recommended recipe history for given user', description="db_delete", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the user id to clear recommendation history')])

class UpdateRecRecipeDate(Form):
    userInfo = TextField(label='Username and recipe id to change recipe date', description="db_update", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the username of user and the recipe id to update and update date recommended')])

class EnterRecipeInfo(Form):
    recipeInfo = TextField(label='Title and description of the recipe', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=1024, message=u'Enter the title and description of recipe')])

class GetRecRecipe(Form):
    userRetrieve = TextField(label='Username of user to recommend recipes for', description="db_get", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter the username of the user to recommend recipes for')])
