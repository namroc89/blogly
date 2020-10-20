from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserRoutesTestCase(TestCase):
    """Test for views """

    def setUp(self):
        """add sample user"""

        User.query.delete()

        user = User(first_name="Denzel",
                    last_name="Washington", image_url=None)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any bad transaction"""

        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Denzel', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Denzel Washington</h1>', html)
            self.assertIn(
                '<img src="https://www.lococrossfit.com/wp-content/uploads/2019/02/user-icon.png" alt="">', html)

    def test_add_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "Bill", "last_name": "Murry",
                 "image": "https://www.lococrossfit.com/wp-content/uploads/2019/02/user-icon.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Bill Murry", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Denzel Washington", html)
