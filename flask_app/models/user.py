from unittest import result
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session, redirect, render_template
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#CREATE USER - sql/model
    
    @classmethod 
    def create_user(cls, data):
        if not cls.validate_user(data):
            print("User exists!")
            return False
        data = cls.user_data(data)
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s) ;"
        MySQLConnection(cls.db).query_db(query,data)
        user = User.get_user_by_email(data['email'])
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['email'] = user.email
        return user.id



#READ USER - sql/model
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = "SELECT * from users WHERE email = %(email)s ;"
        result = MySQLConnection(cls.db).query_db(query,data)
        if result:
            print(result)
            result = cls(result[0])
        return result

    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])


    @classmethod
    def login_user(cls, data):
        user = cls.get_user_by_email(data['email'])
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                session['last_name'] = user.last_name
                session['email'] = user.email
                return True
        flash('Your login information is incorrect')
        return False
            

#UPDATE Model    

#parsing the users data into the variable user_input_data (see create_user method above)
    @staticmethod
    def user_data(data):
        user_input_data = {
            'first_name' : data ['first_name'],
            'last_name' : data ['last_name'],
            'email' : data ['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return user_input_data




#VALIDATION
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2 :
            flash('Your first name needs to at least 2 characters long.')
            is_valid = False
        if len(data['last_name']) < 2 :
            flash('Your last name needs to at least 2 characters long.')
            is_valid = False
        if len(data['password']) < 8 :
            flash('Your password needs to at least 8 characters long.')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash('Please use valid email')
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('Email already in use')
            is_valid = False
        return is_valid


    
#DELETE Model    

    
    
    

