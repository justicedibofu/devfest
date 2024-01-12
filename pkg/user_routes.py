from datetime import datetime
import os,random,string
from functools import wraps
from flask import render_template, abort, request, redirect, flash, url_for, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app 

from pkg.models import db, User, Level

def login_required(f):
    @wraps(f) #this ensures that details (such as __name__) about the original function f, that is being decorated is still available...
    def check_login(*args,**kwargs):
        if session.get("useronline") != None:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in to access this page", category="error")
            return redirect(url_for("login_page"))
    return check_login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    else: #retrieve form fields
        state = request.form.get('state')
        lga = request.form.get('lga')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        hashed_pwd = generate_password_hash(pwd)

        if email != '' and state != '' and lga != '':
            user = User(user_fname=fname,user_lname=lname,user_email=email,user_password=hashed_pwd,user_stateid=state,user_lgaid=lga)
            db.session.add(user)
            db.session.commit()
            id = user.user_id
            session['useronline'] = id
            return redirect('/dashboard') #insert into database
        else:
            flash ("Please fill all the fields", category='error')
            return redirect(url_for('register'))
        

@app.route('/logout')
def user_logout():
    if session.get("useronline") != None:
        session.pop("useronline", None)
    return redirect('/')

@app.route('/')
@login_required
def homepage():
    return render_template('user/index.html')

@app.route('/dashboard')
@login_required
def user_dashboard():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/dashboard.html', deets=deets)
    
    

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('user/loginpage.html')
    else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        record = db.session.query(User).filter(User.user_email == email).first()
        if record:
            hashed_pwd = record.user_password #the pwd on table
            rsp = check_password_hash(hashed_pwd,pwd)
            if rsp:
                id = record.user_id
                session['useronline'] = id
                return redirect('/dashboard')
            else:
                flash("Incorrect Password", category='error')
                return redirect('/login')
        else:
            flash("Incorrect Email", category='error')
            return redirect('/login')



@app.route('/profile', methods=['GET','POST'])
@login_required
def user_profile():
    id = session.get('useronline')

    
    if request.method == 'GET':
        deets = User.query.get(id)
        devs = db.session.query(Level).all()
        return render_template('user/profile.html', devs=devs, deets=deets)
    else:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        phone = request.form.get('phone')
        level = request.form.get('level')
        update = db.session.query(User).get(id)

        update.user_fname =fname
        update.user_lname = lname
        update.user_phone = phone
        update.user_levelid = level
        db.session.commit()
        return redirect('/profile')
    
@app.route("/changedp", methods=["GET", "POST"])
@login_required
def change_dp():
    id = session['useronline']
    deets = User.query.get(id)
    oldpix = deets.user_pix
    if request.method == "GET":
        return render_template("user/changedp.html", deets=deets)
    else:
        dp = request.files.get('dp')
        filename = dp.filename #empty if no file was seected for upload
        ext = filename.split(".")
        
        if filename == '':
            flash("Please select a file", category='error')
            return redirect("/changedp")
        else:
            name,ext = os.path.splitext(filename)
            allowed = ['.jpg','.png','.jpeg']
            if ext.lower() in allowed:
                final_name = int(random.random() *10000000)
                final_name = str(final_name) + ext #
                dp.save(f"pkg/static/profile/{final_name}") #Go and create a folder in pkg
                user = db.session.query(User).get(id)
                user.user_pix = final_name
                db.session.commit()
                try:
                    os.remove(f"pkg/static/profile/{oldpix}")
                except:
                    pass
                flash("Profile picture added",category="success")
                return redirect('/dashboard')
            else:
                flash("Extension not allowed", category='error')
                return redirect('/changedp')