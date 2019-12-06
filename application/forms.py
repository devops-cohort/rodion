from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from flask_login import LoginManager, current_user



class AddSongForm(FlaskForm):
    title = StringField('Title',
        validators=[
                DataRequired(),
                Length(min=1, max=100)
        ]
    )
    artist = StringField('Artist',
        validators=[
                DataRequired(),
                Length(min=1, max=100)
        ]
    )
    album = StringField('Album',
        validators=[
                DataRequired(),
                Length(min=1, max=100)
        ]
    )
    genre = StringField('Genre',
        validators=[
                DataRequired(),
                Length(min=1, max=100)
        ]
    )

    submit = SubmitField('Add song to library')

class ShowSongForm(FlaskForm):
    title = StringField('Title',
        validators=[
                Length(min=1, max=100)
        ]
    )
    artist = StringField('Artist',
        validators=[
                Length(min=1, max=100)
        ]
    )
    album = StringField('Album',
        validators=[
                Length(min=1, max=100)
        ]
    )
    genre = StringField('Genre',
        validators=[
                Length(min=1, max=100)
        ]
    )
    submit = SubmitField('Find Music')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    first_name = StringField('First Name',
        validators=[
                DataRequired(),
                Length(min=4, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators=[
                DataRequired(),
                Length(min=4, max=30)
        ]
    )
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=4, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')
    submit = SubmitField('Update')
    #delete = SubmitField('Delete')

class SearchForm(FlaskForm):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')
