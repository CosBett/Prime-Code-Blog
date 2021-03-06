import unittest

from app.models import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username='Mandellah',email = "mandellah94@gmail.com", bio ='default bio',password='poi2134')

    def test_password_setter(self):
        self.assertTrue(self.new_user.hashed_passwordis, not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.hashed_password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('poi2134'))


