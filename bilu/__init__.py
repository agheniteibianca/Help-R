from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pymysql
from sqlalchemy_utils import force_instant_defaults


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/bilu?charset=utf8'


UPLOAD_FOLDER = 'bilu/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 15)



class Singleton(object):
    _db = None

    @staticmethod 
    def getInstance():
        if Singleton._db == None:
            Singleton()
        return Singleton._db

    def __init__(self):
        if Singleton._db != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton._db = SQLAlchemy(app)



Singleton()
db = Singleton.getInstance()


##############create dabase###############
from bilu.models import users, service
force_instant_defaults()
db.create_all()



#############import blueprints################
from bilu.home.routes import main
app.register_blueprint(main)

from bilu.servises.routes import services
app.register_blueprint(services)


from bilu.myprofile.routes import myprofile
app.register_blueprint(myprofile)



