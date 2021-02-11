import os

from bilu import app
from bilu.models import db, service, users, profile, categories, orders, service_reviews
from flask import (Blueprint, Flask, Response, flash, redirect,
                   render_template, request, session, url_for)
from werkzeug.utils import secure_filename

services = Blueprint("services", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@services.route('/services_index', methods=["POST", "GET"])
def services_index_display():
	if request.method == "POST":

		values=service.query.all()

		if "view" in request.form:
			received_id=request.form['service_id']
			return redirect(url_for("services.service_page", id = received_id))
		elif "all" in request.form:
			all_categories = categories.query.all()
			return render_template('services_index.html',category=None,  values=service.query.all(), all_categories=all_categories )
		elif "1" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=1).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories  )
		elif "2" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=2).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "3" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=3).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "4" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=4).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "5" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=5).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "6" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=6).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "7" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=7).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "8" in request.form:
			all_categories = categories.query.all()
			found_category = categories.query.filter_by(id=8).first()
			return render_template('services_index.html', category=found_category,values=service.query.all(), all_categories=all_categories )
		elif "search" in request.form:
			search_word = request.form['aaa']
			values=service.query.all()
			found_services = []
			for serv in values:
				if search_word in serv.title or search_word in serv.description:
					found_services.append(serv)
			all_categories = categories.query.all()
			return render_template("services_index.html",category=None, values=found_services , all_categories=all_categories)
		
	else:
		values=service.query.all()
		all_categories = categories.query.all()
		return render_template("services_index.html",category=None, values=service.query.all() , all_categories=all_categories)
		


@services.route('/display/<filename>')
def display_image(filename):
	print(filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)



@services.route('/create_service',)
def create_service():
	if 'user' not in session:
		return redirect(url_for("main.login"))
	return render_template('create_service.html')

@services.route('/create_service', methods=['POST'])
def upload_image():
	if 'user' not in session:
		return redirect(url_for("main.login"))
	if "upload" in request.form:

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)


		if file and allowed_file(file.filename):
			short_filename=secure_filename(file.filename)
			os_filename= 'servises/' + str(session['user']) + '/description_pic/'

			if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], os_filename)):
				os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], os_filename), 0o777)

			os_filename += secure_filename(file.filename)
			session['bilu'] = short_filename
			
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], os_filename))
			flash('Image successfully uploaded')
			return render_template("create_service.html", filename=short_filename)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	elif "add" in request.form:
		users_id=session['user']
		title = request.form['title']
		description = request.form['description']
		category_id = request.form.get('comp_select')
		
		price=1.0;

	
		if 'bilu' in session:
			description_pic = str(session['user']) + "/description_pic/"+ session['bilu']
		else:
			description_pic = ''

		new_service = service(users_id,title,description, price, description_pic,category_id)
		session.pop('bilu', None)

		db.session.add(new_service)
		db.session.commit()
		
		return redirect(url_for("services.services_index_display"))


@services.route('/service/<id>',methods=["POST", "GET"])
def service_page(id):
	if request.method == "POST":
		if 'user' not in session:
			return redirect(url_for("main.login"))
		else:
			if "order" in request.form:
				
				found_service = service.query.filter_by(id=id).first()
				owner_id = 	found_service.users_id
				owner = users.query.filter_by(id=owner_id).first()
				found_profile = profile.query.filter_by(user_id=owner_id).first()
				all_services = service.query.filter_by(users_id=owner_id)


				session.pop('_flashes', None)
				flash("Comanda plasata!")

				new_order = orders(session['user'],id,False)
				db.session.add(new_order)
				db.session.commit()

				return render_template("service_page.html", user=owner, profile=found_profile, service=found_service, services=all_services)
			elif "contact" in request.form:
				found_service = service.query.filter_by(id=id).first()
				owner_id = 	found_service.users_id
				all_profiles = profile.query.filter_by(user_id=id).all()
				return redirect(url_for("myprofile.compose_message", id = owner_id, all_profiles=all_profiles ))
			elif "view" in request.form:
				received_id=request.form['service_id']
				return redirect(url_for("services.service_page", id = received_id))
				
							
	
	else:
		session.pop('_flashes', None)
		found_service = service.query.filter_by(id=id).first()
		owner_id = 	found_service.users_id
		owner = users.query.filter_by(id=owner_id).first()

		found_profile = profile.query.filter_by(user_id=owner_id).first()
		all_services = service.query.filter_by(users_id=owner_id)

		all_profiles = profile.query.all()
		all_users = users.query.all()

		reviews = service_reviews.query.filter_by(services_id=found_service.id)


		return render_template("service_page.html", user=owner, profile=found_profile, service=found_service, services=all_services, all_profiles=all_profiles, all_users=all_users, reviews=reviews)
        
	