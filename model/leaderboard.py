# leaderboard.py
import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from sqlalchemy.exc import IntegrityError
from model.user import User
from model.channel import Channel
from __init__ import app, db
class Leaderboard(db.Model):
    """
    Post Model
    The Post class represents an individual contribution or discussion within a channel.
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _title (db.Column): A string representing the title of the post.
        _comment (db.Column): A string representing the comment of the post.
        _content (db.Column): A JSON blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
    """
    __tablename__ = 'leaderboards'
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _comment = db.Column(db.String(255), nullable=False)
    _content = db.Column(JSON, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __init__(self, title, comment, user_id=None, content={}, user_name=None):
        """
        Constructor, 1st step in object creation.
        Args:
            title (str): The title of the post.
            comment (str): The comment of the post.
            user_id (int): The user who created the post.
            content (dict): The content of the post.
        """
        self._title = title
        self._comment = comment
        self._user_id = user_id
        self._content = content
    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Leaderboard(id={self.id}, title={self._title}, comment={self._comment}, content={self._content}, user_id={self._user_id})"
    def create(self):
        """
        Creates a new post in the database.
        Returns:
            Post: The created post object, or None on error.
        """
        try:
            db.session.add(self)
            db.session.commit()
            print (f"Record successfully added: {self}")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create post with title '{self._title}' due to {str(e)}.")
            return None
        return self
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        Uses:
            The Channel.query and User.query methods to retrieve the channel and user objects.
        Returns:
            dict: A dictionary containing the post data, including user and channel names.
        """
        user = User.query.get(self._user_id)
        data = {
            "id": self.id,
            "title": self._title,
            "comment": self._comment,
            "content": self._content,
            "user_name": user.name if user else None,
        }
        return data
    def update(self):
        """
        Updates the post object with new data.
        Args:
            inputs (dict): A dictionary containing the new data for the post.
        Returns:
            Post: The updated post object, or None on error.
        """
        inputs = Leaderboard.query.get(self.id)
        title = inputs._title
        content = inputs._content
        user_name = User.query.get(inputs._user_id).name if inputs._user_id else None
        if user_name:
            user = User.query.filter_by(_name=user_name).first()
            if user:
                user_id = user.id
            else:
                return None
        # Update table with new data
        if title:
            self._title = title
        if content:
            self._content = content
        if user_id:
            self._user_id = user_id
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update post with title '{title}' due to missing channel_id.")
            return None
        return self
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        Uses:
            The db ORM methods to delete and commit the transaction.
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    @staticmethod
    def restore(data):
        for post_data in data:
            _ = post_data.pop('id', None)  # Remove 'id' from post_data
            title = post_data.get("title", None)
            post = Leaderboard.query.filter_by(_title=title).first()
            if post:
                post.update(post_data)
            else:
                post = Leaderboard(**post_data)
                post.update(post_data)
                post.create()
def initLeaderboards():
    """
    The initSandiegos function creates the Post table and adds tester data to the table.
    Uses:
        The db ORM methods to create the table.
    Instantiates:
        Post objects with tester data.
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        leaderboards = [
            Leaderboard(title='fourth place', comment='10 wins', content={'type': 'announcement'}, user_id=1),
            Leaderboard(title='fifth place', comment='9 wins', content={'type': 'announcement'}, user_id=2),
            Leaderboard(title='sixth place', comment='8 wins', content={'type': 'announcement'}, user_id=3),
        ]
        for i in leaderboards:
            print(f"Attempting to create record: {repr(i)}")
            try:
                i.create()
                print(f"Record created: {repr(i)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {i._title}")