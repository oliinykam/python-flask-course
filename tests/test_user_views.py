import unittest
from app import create_app, db
from app.posts.models import User

class UserAuthTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Реєстрація', response.data.decode('utf-8'))

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вхід в систему', response.data.decode('utf-8'))

    def test_register_user(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secret1',
            'confirm_password': 'secret1'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        user = db.session.scalar(db.select(User).where(User.username == 'testuser'))
        self.assertIsNotNone(user, "Користувач не був створений у базі даних")
        self.assertEqual(user.email, 'test@example.com')

    def test_login_user(self):
        self.client.post('/register', data={
            'username': 'loginuser',
            'email': 'login@example.com',
            'password': 'secret1',
            'confirm_password': 'secret1'
        }, follow_redirects=True)

        response = self.client.post('/login', data={
            'username': 'loginuser',
            'password': 'secret1'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Акаунт', response.data.decode('utf-8')) 
        self.assertIn('loginuser', response.data.decode('utf-8'))

    def test_logout(self):
        self.client.post('/register', data={
            'username': 'logoutuser',
            'email': 'out@example.com',
            'password': 'secret1',
            'confirm_password': 'secret1'
        }, follow_redirects=True)

        self.client.post('/login', data={
            'username': 'logoutuser',
            'password': 'secret1'
        }, follow_redirects=True)

        response = self.client.get('/logout', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вхід', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()