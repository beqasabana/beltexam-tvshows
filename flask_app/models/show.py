from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Show:
    def __init__(self, data, author_cls = None):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author = author_cls
        self.liked_by = []

    def get_likes(self):
        data = {
            'id': self.id
        }
        query = "SELECT * FROM shows LEFT JOIN likes ON shows.id = likes.show_id WHERE id = %(id)s;"
        results = connectToMySQL('tvshows').query_db(query, data)
        if results:
            for result in results:
                if result['likes.user_id']:
                    self.liked_by.append(result['likes.user_id'])


    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (user_id, title, network, release_date, description) VALUES(%(user_id)s, %(title)s, %(network)s, %(release_date)s, %(description)s);"
        show_id = connectToMySQL('tvshows').query_db(query, data)
        return show_id

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM shows JOIN users ON users.id = user_id WHERE shows.id = %(id)s;"
        show = connectToMySQL('tvshows').query_db(query, data)
        if show:
            author = user.User({
                'id': show[0]['id'],
                'first_name': show[0]['first_name'],
                'last_name': show[0]['last_name'],
                'email': show[0]['email'],
                'password': show[0]['password'],
                'created_at': show[0]['users.created_at'],
                'updated_at': show[0]['users.updated_at']
            })
            show_cls = cls(show[0], author)
            show_cls.get_likes()
            return show_cls
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        shows_in_db = connectToMySQL('tvshows').query_db(query)
        shows_cls = []
        for show in shows_in_db:
            shows_cls.append(cls(show))
            shows_cls[-1].get_likes()
        return shows_cls

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows WHERE shows.id = %(id)s"
        result = connectToMySQL('tvshows').query_db(query, data)
        return result

    @classmethod
    def edit(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s  WHERE id = %(id)s;"
        result = connectToMySQL('tvshows').query_db(query, data)
        return result
    
    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, show_id) VALUES (%(user_id)s, %(show_id)s);"
        result = connectToMySQL('tvshows').query_db(query, data)
        return result

    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND show_id = %(show_id)s;"
        result = connectToMySQL('tvshows').query_db(query, data)
        return result

    @staticmethod
    def validate_show(form):
        is_valid = True
        if len(form['title']) < 3:
            flash("Title is Required and must be at leaset 3 characters.", 'show-error')
            is_valid = False
        if len(form['network']) < 3:
            flash("Network is Required and must be at leaset 3 characters.", 'show-error')
            is_valid = False
        if len(form['release_date']) == 0:
            flash("Release date is Required.", 'show-error')
            is_valid = False
        if len(form['description']) < 3:
            flash("Description is Required and must be at leaset 3 characters", 'show-error')
            is_valid = False
        return is_valid