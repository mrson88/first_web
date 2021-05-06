from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#tao Flash instance
app=Flask(__name__)
app.config['SECRET_KEY']='my super secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db =SQLAlchemy(app)

#create_model
class Users(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120),nullable=False,unique=True)
    date_added=db.Column(db.DateTime,default=datetime.utcnow)

    #Create a String
    def __repr__(self):
        return '<Name: %r>' % self.name

# tao Form class
class UserForm(FlaskForm):

    name=StringField('Name',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit=SubmitField('Submit')

class NameForm(FlaskForm):

    name=StringField('What your name',validators=[DataRequired()])
    submit=SubmitField('Submit')



# tao 1 route decorator
@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name=None
    form = UserForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user=Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.email.data=''
        flash('User Successfull added')
    our_users=Users.query.order_by(Users.date_added)
    return render_template('add_user.html',form=form,name=name,our_users=our_users)


@app.route('/')
def index():
    firstname='Mr Son'
    stuff='This is Bold text'
    favorite_pizza=["pizza_ca","pizza_ga","pizaa_cho","pizza_meo",41]
    return render_template('index.html',firstname=firstname,stuff=stuff
                           ,favorite_pizza=favorite_pizza)
@app.route('/user/<name>')
def user(name):

    return render_template('user.html',first_name=name)

# Custom Error Page


# Invalid Url
@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def pagenotfound(e):
    return render_template('500.html'),500
@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash('Form Submited Successfull')
    return render_template('name.html',name=name,form=form)


if __name__ == '__main__':
    app.run(debug=True)