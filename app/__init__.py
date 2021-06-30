# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, session, jsonify
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
import os
import sqlite3


from func.img_base64 import img_base64
from func.datetime_display import datetime_display, get_today
from func.sql_connect import sql_connect


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'secret key'
events_path = os.path.join('database', 'events.db')


class InfoForm(FlaskForm):
    input_date = DateField('Input Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    time_message = datetime_display()
    return render_template('portal.html', time_message=time_message)


@app.route('/calendar')
def calendar():
    date_today = get_today()
    time_message = datetime_display()
    connection = sqlite3.connect(events_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events")
    keys = list(map(lambda x: x[0], cursor.description))
    cursor.execute("SELECT * FROM events ORDER BY id")
    values = cursor.fetchall()
    events = []
    for value in values:
        events.append(dict(zip(keys, value)))
    print(events)
    cursor.close()
    connection.commit()
    connection.close()
    return render_template('test.html', date_today=date_today, 
                           time_message=time_message, events=events)

@app.route('/calendar/insert', methods=['POST', 'GET'])
def insert():
    connection = sqlite3.connect(events_path)
    cursor = connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        cost = request.form['cost']
        cursor.execute("INSERT INTO events (title, start_event, end_event, cost) VALUES (%s, %s, %s, %s)", [title, start, end, cost])
        cursor.close()
        connection.commit()
        connection.close()
        msg = 'success'
    return jsonify(msg)

@app.route('/calendar/update', methods=['POST', 'GET'])
def update():
    connection = sqlite3.connect(events_path)
    cursor = connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        cost = request.form['cost']
        id = request.form['id']
        cursor.execute("UPDATE events SET title = %s, start_event = %s, end_event = %s, cost = %s, WHERE id = %s ", [title, start, end, cost, id])
        cursor.close()
        connection.commit()
        connection.close()
        msg = 'success'
    return jsonify(msg)

@app.route('/calendar/ajax_delete',methods=['POST','GET'])
def ajax_delete():
    connection = sqlite3.connect(events_path)
    cursor = connection.cursor()
    if request.method == 'POST':
        getid = request.form['id']
        cursor.execute("DELETE FROM events WHERE id = {0}".format(getid))
        cursor.close()
        connection.commit()
        connection.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)





@app.route('/flight', methods=['GET', 'POST'])
def flight():
    input_date = None
    flights = None
    time_message = datetime_display()
    form = InfoForm()
    if form.validate_on_submit():
        session['input_date'] = form.input_date.data
        input_date = session['input_date']
    if input_date:
        from func.flight_render import crawl_start
        flights = crawl_start('Ctrip', input_date)
    return render_template('flight.html', time_message=time_message, form=form, input_date=input_date,
                           flights=flights)


@app.route('/flight', methods=['GET', 'POST'])
def date():
    time_message = datetime_display()
    input_date = session['input_date']
    return render_template('flight.html', time_message=time_message)





@app.route('/baggage')
def baggage():
    time_message = datetime_display()
    return render_template('baggage.html', time_message=time_message)


@app.route('/cost_estimation')
def cost_estimation():
    time_message = datetime_display()
    return render_template('cost_estimation.html', time_message=time_message)


@app.route('/others')
def others():
    time_message = datetime_display()
    tb_policies = sql_connect('policies')
    tb_links = sql_connect('links')
    return render_template('others.html', time_message=time_message,
                           tb_policies=tb_policies,
                           tb_links=tb_links)
