from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session

class Post:
    db = 'exam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.message = data['message']
        self.quantity = data['quantity']
        self.sighting_date = data['sighting_date']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.users_id = data['users_id']

#Validate

    @staticmethod
    def validate_post(posts):
        is_valid = True
        if len(posts['location']) <= 0:
            is_valid = False
            flash("Input in all fields required")
        if len(posts['message']) <= 0:
            is_valid = False
            flash("Input in all fields required")
        if len(posts['quantity']) =="":
            is_valid = False
            flash("Must have seen more than 1!")
        if len(posts['sighting_date']) == "":
            is_valid = False
            flash("Date is required")
        return is_valid



#CREATE models
    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (location, message, quantity, sighting_date, users_id) VALUES (%(location)s, %(message)s, %(quantity)s, %(sighting_date)s, %(users_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

        

#READ models

    @classmethod
    def show_by_id(cls,data):
        query = "SELECT * FROM posts WHERE id = %(post_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])


    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM posts;"
        results = connectToMySQL(cls.db).query_db(query)
        all_posts = []
        for row in results:
            print(row['users_id'])
            all_posts.append ( cls(row) )
        return all_posts



#UPDATE models
    @classmethod
    def edit_post(cls, data):
        query = "UPDATE posts SET location=%(location)s, message= %(message)s, quantity=%(quantity)s, sighting_date=%(sighting_date)s, users_id=%(users_id)s, updated_at=NOW(), created_at=NOW() WHERE id = %(post_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results





#DELETE models
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM posts WHERE id = %(post_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        # return results
