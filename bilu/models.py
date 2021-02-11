from bilu import db
import datetime
#model

 
 
class pms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id_from = db.Column("users_id_from", db.Integer, db.ForeignKey('users.id'), nullable=False)
    users_id_to = db.Column("users_id_to", db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_time =db. Column("date_time", db.DateTime, default=datetime.datetime.utcnow)
    message =db.Column("message", db.Text)

    def __init__(self,users_id_from,users_id_to,date_time,message):
        self.users_id_from = users_id_from    
        self.users_id_to = users_id_to
        self.date_time = date_time
        self.message = message

   

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    name = db.Column("name", db.String(100), nullable=False)
    password = db.Column("password", db.String(100))
    email = db.Column("email", db.String(100), default="default")
    extra = db.Column("extra", db.String(100))


    services = db.relationship('service', backref='service', lazy=True)
    orders = db.relationship('orders', backref='orders', lazy=True)
    


    from_user = db.relationship(pms,foreign_keys=pms.users_id_from, backref='pms1', lazy=True)
    to_user = db.relationship(pms,foreign_keys=pms.users_id_to, backref='pms2', lazy=True)
    
    reviews = db.relationship('service_reviews', backref='reviews1', lazy=True)

    def __init__(self,name,password,email):
        self.name = name    
        self.password = password
        self.email = email
    def __repr__(self):
        return f"User(' {self.name}', '{self.password}')"



class service(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)

    users_id = db.Column("users_id", db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column("category_id", db.Integer, db.ForeignKey('categories.id'), nullable=False)
    

    title = db.Column("title", db.String(45), nullable=False)
    description = db.Column("description", db.Text, nullable=True)
    price = db.Column("price", db.Float, nullable=False)
    upvotes = db.Column("upvotes", db.Integer, server_default="0")
    downvotes = db.Column("downvotes", db.Integer, server_default="0")
    is_promoted = db.Column("is_promoted", db.Boolean)
    description_pic =db.Column("description_pic", db.Text)

    reviews = db.relationship('service_reviews', backref='reviews2', lazy=True)


    def __init__(self,users_id,title,description, price, description_pic,category_id):
        self.users_id = users_id
        self.title = title
        self.description = description
        self.price = price
        self.description_pic = description_pic
        self.category_id = category_id


    def __repr__(self):
        return repr('Hello ' + self.title )


class orders(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    users_id = db.Column("users_id", db.Integer, db.ForeignKey('users.id'), nullable=False)
    services_id = db.Column("services_id", db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    is_completed = db.Column("is_completed", db.Boolean)


    def __init__(self,users_id,services_id,is_completed):
        self.users_id = users_id
        self.services_id = services_id
        self.is_completed = is_completed
        

class profile(db.Model):
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'),  primary_key=True, nullable=False)


    email = db.Column("email", db.String(45), nullable=True)
    first_name = db.Column("first_name", db.String(45), nullable=True)
    surname = db.Column("surname", db.String(45), nullable=True)
    age = db.Column("age", db.Integer, nullable=True)
    rating = db.Column("rating", db.Float, nullable=True)
    profile_pic = db.Column("profile_pic", db.Text, nullable=True)
    bio = db.Column("bio", db.Text, nullable=True)
    country = db.Column("country", db.String(45), nullable=True)
    city = db.Column("city", db.String(45), nullable=True)
    phone_number = db.Column("phone_number", db.String(45), nullable=True)

    def __init__(self,user_id,email):
        self.user_id = user_id
        self.email = email
   


class categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    services = db.relationship('service', backref='service2', lazy=True)

class service_reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    services_id = db.Column("services_id", db.Integer, db.ForeignKey('service.id'), nullable=False)
    services_users_id = db.Column("services_users_id", db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column("title", db.String(45), nullable=True)
    description = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Integer)
 

    def __init__(self,services_id,services_users_id, title, description, grade):
        self.services_id = services_id
        self.services_users_id = services_users_id
        self.title = title
        self.description = description
        self.grade = grade


 