from flask import render_template,redirect, url_for, request
from application import app, db
from application.models import Users, Songs
#Posts in previous import
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, SongForm
#PostForm in previous import
from application import app,db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

#@app.route('/')
@app.route('/home')
def home():
    #postData = Posts.query.all()
    #posts=postData
    return render_template('home.html', title = 'Home')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('about')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

    return render_template('login.html', title = 'Login',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            first_name=form.first_name.data, 
            last_name=form.first_name.data,
            email=form.email.data,
            password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('about'))
    return render_template('register.html', title = 'Register', form=form)


@login_required
@app.route('/songs', methods=['GET','POST'])
def songs():
    form = SongForm()
    if request.method == 'POST':
        song = Songs(
                title=form.title.data,
                artist=form.artist.data,
                album=form.album.data,
                genre=form.genre.data)
    
        db.session.add(song)i
        db.session.commit()
    return render_template('songs.html', title='Songs', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)

dummyData = [
    {
        "name": {"first":"Chester", "last":"Gardner"},
        "title":"First Post",
        "content":"This is some dummy data for Flask lectures"
    },
    {
        "name": {"first":"Chris", "last":"Perrins"},
        "title":"Second Post",
        "content":"This is even more dummy data for Flask lectures"
    }
]
