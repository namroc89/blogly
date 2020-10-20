from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTest(TestCase):
    """Tests the User model"""

    def setUp(self):
        """Clean up existing users"""

        User.query.delete()

    def tearDown(self):
        """Clean up any bad transaction"""

        db.session.rollback()

    def test_get_full_name(self):
        """Check if get_full_name returns full name"""
        user = User(first_name="Testfirst",
                    last_name="Testlast", image_url=None)
        self.assertEquals(user.get_full_name(), "Testfirst Testlast")
