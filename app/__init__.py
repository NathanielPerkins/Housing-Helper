from flask import Flask

app = Flask(__name__)
from app import views

app.secret_key = 'some secret key'