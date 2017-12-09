from app import app
from flask import render_template, request
from wtforms import Form, StringField
from os import environ


API = environ["GOOGLE_EMBED_API_KEY"]


def clean_location_string(unclean):
    return unclean.replace(" ", "+")


class input_form(Form):
    source = StringField('Source Address')
    destination1 = StringField('Public Transport Address 1')
    destination2 = StringField('Public Transport Address 2')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = input_form(request.form)
    if request.method == 'POST' and form.validate(): 
        source = clean_location_string(form.source.data)
        destination1 = clean_location_string(form.destination1.data)
        destination2 = clean_location_string(form.destination2.data)
        directions1 = build_direction_string(source, destination1)
        directions2 = build_direction_string(source, destination2)
        sup = build_supermarket_string(source)
        return render_template('app.html', travel1=directions1, 
                               travel2=directions2, supermarkets=sup,
                               form=form)
    return render_template('app.html', form=form)


def build_supermarket_string(source):
    base_str = "https://www.google.com/maps/embed/v1/search?key=" 
    to_request = base_str + API
    to_request = to_request + '&q=supermarkets+near+{}'.format(source)
    return to_request


def build_direction_string(source, destination):
    base_str = "https://www.google.com/maps/embed/v1/directions?key=" 
    to_request = base_str + API
    to_request = to_request + '&origin={}'.format(source)
    to_request = to_request + '&destination={}'.format(destination)
    to_request = to_request + '&mode=transit'
    return to_request
