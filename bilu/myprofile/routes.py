import os
import datetime
from bilu import app
from bilu.models import db, service, users, profile, orders, pms, service_reviews
from flask import (Blueprint, Flask, Response, flash, redirect,
                   render_template, request, session, url_for)
from werkzeug.utils import secure_filename

myprofile = Blueprint("myprofile", __name__)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@myprofile.route('/display/<filename>')
def display_image(filename):
	print(filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@myprofile.route('/myprofile', methods=["POST", "GET"])
def myprofile_display():
    if 'user' not in session:
        return redirect(url_for("main.login"))

    
    if request.method == "POST":
        if "edit" in request.form:
            edit_mode=1

            found_profile = profile.query.filter_by(user_id=session["user"]).first()
            found_services = service.query.filter_by(users_id=session["user"]).all()
            all_services = service.query.all()


            all_orders = []
            for ser in found_services:
                service_id = ser.id
                found_orders = orders.query.filter_by(services_id=service_id).all()
                for item in found_orders:
                    all_orders.append(item)
            found_services = service.query.filter_by(users_id=session["user"])
            return render_template("myprofile.html", id=session["user"], profile=found_profile, services=found_services, all_services=all_services, edit_mode=edit_mode, orders=all_orders)
    
        elif "done" in request.form:
            edit_mode=0

            #edit the info
            new_age = request.form['new_age']
            if (new_age == ""):
                new_age = 0
            new_country = request.form['new_country']
            new_city = request.form['new_city']
            new_number = request.form['new_number']
            new_description = request.form['new_description']
            new_name = request.form['new_name']
            new_surname = request.form['new_surname']

            current_profile = profile.query.filter_by(user_id=session["user"]).first()
            current_profile.age = new_age
            current_profile.bio = new_description
            current_profile.country = new_country
            current_profile.city = new_city
            current_profile.phone_number = new_number
            current_profile.first_name = new_name
            current_profile.surname = new_surname
            db.session.commit()

            found_profile = profile.query.filter_by(user_id=session["user"]).first()
            found_services = service.query.filter_by(users_id=session["user"]).all()
            all_services = service.query.all()


            all_orders = []
            for ser in found_services:
                service_id = ser.id
                found_orders = orders.query.filter_by(services_id=service_id).all()
                for item in found_orders:
                    all_orders.append(item)
            found_services = service.query.filter_by(users_id=session["user"])
            return render_template("myprofile.html", id=session["user"], profile=found_profile, services=found_services, all_services=all_services, edit_mode=edit_mode, orders=all_orders)
    
        elif "mark" in request.form:
            edit_mode=0

            order_id=request.form['order_id']
            found_order = orders.query.filter_by(id=order_id).first()
            found_order.is_completed = True;
            db.session.commit()

        
            return redirect(url_for("myprofile.myprofile_display"))
        elif "inbox" in request.form:
            return redirect(url_for("myprofile.inbox"))
        elif "orders" in request.form:
            return redirect(url_for("myprofile.my_orders"))
        elif "logout" in request.form:
            return redirect(url_for("main.logout"))

        elif "upload" in request.form:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                
                
                flash('No image selected for uploading')
                return redirect(request.url)


            if file and allowed_file(file.filename):
                short_filename=secure_filename(file.filename)
                os_filename= 'profile/' + str(session['user']) + '/'

                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], os_filename)):
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], os_filename), 0o777)

                os_filename += secure_filename(file.filename)
                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], os_filename))
                flash('Image successfully uploaded')

                #change database
                new_pic_path = str(session['user']) + '/' + secure_filename(file.filename)
                current_profile = profile.query.filter_by(user_id=session["user"]).first()
                current_profile.profile_pic = new_pic_path
                db.session.commit()

                return redirect(url_for("myprofile.myprofile_display"))
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif')
                return redirect(request.url)
        else:
            return redirect(url_for("services.create_service"))
    else:
        edit_mode=0
        found_profile = profile.query.filter_by(user_id=session["user"]).first()
        found_services = service.query.filter_by(users_id=session["user"]).all()
        all_services = service.query.all()


        all_orders = []
        for ser in found_services:
            service_id = ser.id
            found_orders = orders.query.filter_by(services_id=service_id).all()
            for item in found_orders:
                all_orders.append(item)
        found_services = service.query.filter_by(users_id=session["user"])

        return render_template("myprofile.html", id=session["user"], profile=found_profile, services=found_services, all_services=all_services, edit_mode=edit_mode, orders=all_orders)
    

@myprofile.route('/compose_message/<id>', methods=["POST", "GET"])
def compose_message(id):
    if 'user' not in session:
        return redirect(url_for("main.login"))
    if request.method == "POST":
        if "send" in request.form:
            body = request.form['body']
            #add new message
            new_msg = pms(session["user"],id,datetime.datetime.now(),body)
            db.session.add(new_msg)
            db.session.commit()
        return redirect(url_for("myprofile.inbox"))
    else:
        found_user = users.query.filter_by(id=id).first()
        all_profiles = profile.query.all()
        return render_template("compose_message.html",all_profiles = all_profiles, id=id)
   

@myprofile.route('/inbox', methods=["POST", "GET"])
def inbox():
    if 'user' not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        if "reply" in request.form:
            new_to_user_id=request.form['user']
            return redirect(url_for("myprofile.compose_message", id = new_to_user_id))
        elif "delete" in request.form:
            pm_id=request.form['pm_id']
            pm_to_be_deleted = pms.query.filter_by(id=pm_id).delete()
            db.session.commit()
            return redirect(url_for("myprofile.inbox"))
        elif "sent" in request.form:
            return redirect(url_for("myprofile.sent"))
        else:
            found_pms = pms.query.filter_by(users_id_to=session["user"])
            all_users = users.query.all()
            all_profiles = profile.query.all()
            return render_template("inbox.html", id=session["user"], pms=found_pms, all_users=all_users, all_profiles=all_profiles)
    else:
        found_pms = pms.query.filter_by(users_id_to=session["user"])
        all_users = users.query.all()
        all_profiles = profile.query.all()
        return render_template("inbox.html", id=session["user"], pms=found_pms, all_users=all_users, all_profiles=all_profiles)


@myprofile.route('/sent_messages', methods=["POST", "GET"])
def sent():
    if 'user' not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        if "delete" in request.form:
            pm_id=request.form['pm_id']
            pm_to_be_deleted = pms.query.filter_by(id=pm_id).delete()
            db.session.commit()
            return redirect(url_for("myprofile.inbox"))
        elif "received" in request.form:
            return redirect(url_for("myprofile.inbox"))
        else:
            found_pms = pms.query.filter_by(users_id_to=session["user"])
            all_users = users.query.all()
            all_profiles = profile.query.all()
            return render_template("inbox.html", id=session["user"], pms=found_pms, all_users=all_users, all_profiles=all_profiles)
    else:
        found_pms = pms.query.filter_by(users_id_from=session["user"])
        all_users = users.query.all()
        all_profiles = profile.query.all()
        return render_template("sent_messages.html", id=session["user"], pms=found_pms, all_users=all_users, all_profiles=all_profiles)



@myprofile.route('/my_orders', methods=["POST", "GET"])
def my_orders():
    if 'user' not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        if "review" in request.form:
            order_id = request.form["order_id"]
            the_order = orders.query.filter_by(id=order_id).first()

            the_service = the_order.services_id
            return redirect(url_for("myprofile.write_review", id = the_service))
    else:
        found_services = service.query.all()
        all_orders = orders.query.filter_by(users_id=session["user"])
        return render_template("my_orders.html", id=session["user"], orders=all_orders, services=found_services)
        
@myprofile.route('/write_review/<id>', methods=["POST", "GET"])
def write_review(id):
    if 'user' not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":

        body = request.form['body']
        title = request.form['title']

        new_review = service_reviews(id,session["user"],title,body,3)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("myprofile.my_orders"))
    else:
        found_services = service.query.filter_by(users_id=session["user"]).all()
        all_orders = []
        for ser in found_services:
            service_id = ser.id
            found_orders = orders.query.filter_by(services_id=service_id).all()
            for item in found_orders:
                all_orders.append(item)
        found_services = service.query.filter_by(users_id=session["user"])
        return render_template("write_review.html", id=session["user"], orders=all_orders, services=found_services)
     