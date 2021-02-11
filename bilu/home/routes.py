import os
from flask import Blueprint
from flask import Flask, redirect, url_for, render_template, request, session, flash, Response
from bilu.models import db, users, profile
from bilu import app
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__ )

@main.route("/", methods=["POST", "GET"])
def start():
    return redirect(url_for("main.login"))

@main.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if "login" in request.form:
            session.permanent = False
            user = request.form['nm']
            password = request.form['pw']
            found_user = users.query.filter_by(name=user, password=password).first()
            if found_user:
                session["user"] = found_user.id
                session["email"] = found_user.email
                flash("Login succesfull!")
                return redirect(url_for("myprofile.myprofile_display"))
            else:
                flash("Parola incorecta! Doriti sa va inregistrati?")
                return redirect(url_for("main.login"))
        elif "register" in request.form:
            return redirect(url_for("main.register"))
    else:  
        if "user" in session:   #daca ma duc pe login si sunt deja logata
            flash("Already Logged in!")
            return redirect(url_for("myprofile.myprofile_display"))
        return render_template("login.html")

@main.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        session.permanent = False
        user = request.form['nm']
        password = request.form['pw']
        email = request.form['em']

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session.pop('_flashes', None)
            flash("Username taken!")
            return render_template("register.html")
            
        else:
            #add new user to database
            usr = users(user,password,email)
            db.session.add(usr)
            db.session.commit()

            #create empty user profile
            new_id = users.query.filter_by(name=user).first().id
            new_profile = profile(new_id,email)
            db.session.add(new_profile)
            db.session.commit()
            
            session.pop('_flashes', None)
            flash("Registered! You can login now")
            return redirect(url_for("main.login"))
    else:  
        if "user" in session:   #daca ma duc pe login si sunt deja logata
            session.pop('_flashes', None)
            flash("Already Logged in!")
            return redirect(url_for("myprofile.myprofile_display"))
        return render_template("register.html")


@main.route("/logout")
def logout():
    session.pop('_flashes', None)
    flash(f"You have been logged out!" , "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("main.login"))
