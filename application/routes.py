from flask import render_template,redirect, url_for, request
from application import app, db
from application.models import Users, Songs
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddSongForm, ShowSongForm, SearchForm, Results, EditSongForm
from application import app,db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('about')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('search'))

    return render_template('login.html', title = 'Login',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))

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


@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', title = 'Search', form=search)

@app.route('/addsongs', methods=['GET','POST'])
def addsongs():
    form = AddSongForm()
    if request.method == 'POST':
        song = Songs(
                title=form.title.data,
                artist=form.artist.data,
                album=form.album.data,
                genre=form.genre.data,
                user_id=current_user.id)
    
        db.session.add(song)
        db.session.commit()
    return render_template('addsongs.html', title='Add Songs', form=form)


@app.route('/showsongs', methods=['GET'])
def showsongs():
    results = Songs.query.all()
    table = Results(results)
    table.border = True

    return render_template('results.html',table=table)

@app.route('/edit_song/<string:id>', methods=['GET', 'POST'])
def edit_song(id):
    temp =id 
    song=Songs.query.filter_by(id=temp).first()
    print(song)
    form = EditSongForm()
    print(song.title)
    print(form.title.data)
    song.title=form.title.data,
    song.artist=form.artist.data
    song.album=form.album.data
    song.genre=form.genre.data
#    if request.method == 'POST':
#        song = Songs(
#                title=form.title.data,
#                artist=form.artist.data,
#                album=form.album.data,
#                genre=form.genre.data,
#                user_id=current_user.id)
    db.session.commit()
    return render_template('edit_song.html', title='Edit', form=form)
   # else:
   #     return render_template('no_permission.html')



@app.route('/delete_song/<string:id>')
def delete_song(id):
    temp = id
    song=Songs.query.filter_by(id=temp).first()
    if song.user_id == current_user.id:
        db.session.delete(song)
        db.session.commit()
        return redirect(url_for('search'))
    else:
        return render_template('no_permission.html')

@app.route('/results', methods=['GET','POST'])
def search_results(search):
    results = []

    search_string = search.data['search']
    category_string = search.data['select']
    print(search_string)
    if search.data['search'] == '':
        search_string = current_user.id
        print(search_string)
        results = Songs.query.filter_by(user_id=search_string)
        print(results)
        table = Results(results)
        table.border = True
        
    if search.data['search'] != '':
        print('Search for :',search_string)
        print('Search in :',category_string)
        if category_string == 'Title':
            results = Songs.query.filter_by(title=search_string)
            table = Results(results)
            table.border = True
        elif category_string == 'Artist':
            results = Songs.query.filter_by(artist=search_string)
            table = Results(results)
            table.border = True
        elif category_string == 'Album':
            results = Songs.query.filter_by(album=search_string)
            table = Results(results)
            table.border = True
        elif category_string == 'Genre':
            results = Songs.query.filter_by(genre=search_string)
            table = Results(results)
            table.border = True
    return render_template('results.html', table=table)

    if not results:
        print('No results found!')
        return redirect('/search')  

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET','POST'])
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

@app.route('/delete_account', methods=['GET','POST'])
def delete_account():
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('register'))

