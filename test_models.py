from unittest import TestCase

from app import app
from models import User, db

# create database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class bloglyModels(TestCase):
    

    def setUp(self):
        """Clean up any existing users"""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

   

    def test_user(self):
        user = User(first_name="first", last_name="last", picture="url")
        # pet.feed(5)
        user.picture = "lru"
        self.assertEqual(user.picture, "lru")


    def test_get_by_species(self):
        userone = User(first_name="first", last_name="last", picture="url")
        db.session.add(userone)
        db.session.commit()

        user = User.query.get(1)
        self.assertEqual(user.first_name, "first")
