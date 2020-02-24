from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from cfc.User import User
from wtforms.validators import ValidationError

class Signup(FlaskForm):
    netid = StringField("Cornell Netid", validators=[DataRequired()])
    cornell_email = StringField("Cornell Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    type_field = SelectField(" Student / Alumni", choices = [('S','Student'), ('A','Alumni')])
    major = SelectField("Major", choices=[('ECE','Electrical and Computer Engineering'),('CSI','Computer Science')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_netid(self,id):
        user = User.query.filter_by(netid = id.data).first()
        if user :
            raise ValidationError("Net Id already Exists ")

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user :
            raise ValidationError("Email already Exists ")



class Login(FlaskForm):

    cornell_email = StringField("Cornell Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Ref_Post(FlaskForm):
    job_title = StringField("Job Title", validators=[DataRequired()])
    job_des = StringField("Job Description", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])

    submit = SubmitField('POST')

    # def validate_netid(self,id):
    #     user = User.query.filter_by(netid = id.data).first()
    #     if user :
    #         raise ValidationError("Net Id already Exists ")
    #
    # def validate_email(self,email):
    #     user = User.query.filter_by(email = email.data).first()
    #     if user :
    #         raise ValidationError("Email already Exists ")

class SearchQuery(FlaskForm):
    job_title = StringField("Job Title", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])
    search = SubmitField('Search')






