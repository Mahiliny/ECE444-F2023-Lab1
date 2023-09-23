from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


#Add variable to error stmnt !!!!!!!

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired() , Email(message = "Please include an '@' in the email address. Email address is missing an '@' ")] )
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        
        if 'utoronto' in form.email.data:
            valid_email = True
        else:
            valid_email = False
        
        session['email'] = form.email.data
        session['valid_email'] = valid_email

        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), valid_email = session.get('valid_email'))
