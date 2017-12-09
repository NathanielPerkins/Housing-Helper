from app import app
from flask import render_template, request
from wtforms import Form, StringField, SelectField, validators
from os import environ
from re import sub

API = environ["GOOGLE_EMBED_API_KEY"]


def clean_location_string(unclean):
    unclean = sub(r'([0-9])+/', '', unclean)
    return unclean.replace(" ", "+")


class input_form(Form):
    source = StringField('Source Address', [validators.required()])
    destination1 = StringField('Transport Address 1',
                               [validators.required()])
    destination2 = StringField('Transport Address 2')
    near_me = StringField('x Near Me (no argument = "Woolworths and Coles"')
    transport = SelectField(u'Transport Type', choices=[('transit',
                            'Public Transport'), ('driving', 'Car')])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = input_form(request.form)
    if request.method == 'POST' and form.validate():
        source = clean_location_string(form.source.data)
        destination1 = clean_location_string(form.destination1.data)
        destination2 = clean_location_string(form.destination2.data)
        near_me = form.near_me.data
        if near_me is not "":
            near_me = near_me.replace(" ", "+")
        transport = form.transport.data
        directions1 = build_direction_string(source, destination1, transport)
        if destination2 is not "":
            directions2 = build_direction_string(source, destination2,
                                                 transport)
        else:
            directions2 = None
        sup = build_supermarket_string(source, near_me)
        return render_template('app.html', travel1=directions1,
                               travel2=directions2, supermarkets=sup,
                               form=form)
    return render_template('app.html', form=form)


def build_supermarket_string(source, near_me=None):
    base_str = "https://www.google.com/maps/embed/v1/search?key="
    to_request = base_str + API
    if near_me is "":
        near_me = "woolwoorths+and+coles"
    to_request = to_request + '&q={}+near+{}'.format(near_me, source)
    return to_request


def build_direction_string(source, destination, transport):
    base_str = "https://www.google.com/maps/embed/v1/directions?key="
    to_request = base_str + API
    to_request = to_request + '&origin={}'.format(source)
    to_request = to_request + '&destination={}'.format(destination)
    to_request = to_request + '&mode={}'.format(transport)
    return to_request
