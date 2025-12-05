# import unittest
# from app import create_app, db
# from app.posts.models import Post, PostCategory
# from datetime import datetime

# class PostTestCase(unittest.TestCase):
    
#     def setUp(self):
#         """
#         Виконується перед кожним тестом.
#         Створює додаток у 'testing' конфігурації та базу даних у пам'яті.
#         """
#         self.app = create_app("testing") 
#         self.app_context = self.app.app_context()
#         self.app_context.push() 
#         db.create_all()  
#         self.client = self.app.test_client() 

#     def tearDown(self):
#         """
#         Виконується після кожного тесту.
#         Видаляє сесію та всі таблиці, закриває контекст.
#         """
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop() 

#     def _create_dummy_post(self, title="Test Post", content="Test Content", is_active=True):
#         """Допоміжна функція для швидкого створення поста в БД."""
#         post = Post(
#             title=title,
#             content=content,
#             author="Test Author",
#             category=PostCategory.TECH, 
#             is_active=is_active
#         )
#         db.session.add(post)
#         db.session.commit()
#         return post

#     def test_create_post(self):
#         """Тест POST-запиту на /post/create"""
#         response = self.client.post('/post/create', data={
#             'title': 'My First Test Post',
#             'content': 'This is TDD!',
#             'author': 'Unit Test',
#             'category': 'tech',  
#             'posted': datetime.now().strftime('%Y-%m-%dT%H:%M'),
#             'is_active': True 
#         }, follow_redirects=True) 
        
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Пост успішно створено!', response.data.decode('utf-8'))
        
#         post = db.session.scalar(db.select(Post).filter_by(title="My First Test Post"))
#         self.assertIsNotNone(post)
#         self.assertEqual(post.content, "This is TDD!")

#     def test_list_posts(self):
#         """Тест GET-запиту на /post/"""
#         self._create_dummy_post(title="List Test Post")
        
#         response = self.client.get('/post/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"List Test Post", response.data)

#     def test_view_post_detail(self):
#         """Тест GET-запиту на /post/<id>"""
#         post = self._create_dummy_post(content="Detailed Content")
        
#         response = self.client.get(f'/post/{post.id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Detailed Content", response.data)

#     def test_update_post(self):
#         """Тест POST-запиту на /post/<id>/update"""
#         post = self._create_dummy_post()
        
#         response = self.client.post(f'/post/{post.id}/update', data={
#             'title': 'Updated Title',
#             'content': 'Updated Content',
#             'author': 'Updated Author',
#             'category': 'other',
#             'posted': post.posted.strftime('%Y-%m-%dT%H:%M'),
#             'is_active': True
#         }, follow_redirects=True)
        
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Пост успішно оновлено!', response.data.decode('utf-8'))
        
#         updated_post = db.get_or_404(Post, post.id)
#         self.assertEqual(updated_post.title, "Updated Title")
#         self.assertEqual(updated_post.category, PostCategory.OTHER)

#     def test_delete_post(self):
#         """Тест POST-запиту на /post/<id>/delete"""
#         post = self._create_dummy_post()
#         post_id = post.id
        
#         response = self.client.post(f'/post/{post.id}/delete', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Пост успішно видалено.', response.data.decode('utf-8'))
        
#         deleted_post = db.session.get(Post, post_id)
#         self.assertIsNone(deleted_post)

#     def test_404_not_found(self):
#         """Тест GET-запиту на неіснуючий /post/999"""
#         response = self.client.get('/post/999')
#         self.assertEqual(response.status_code, 404)
        
#         response_text = response.data.decode('utf-8')
#         self.assertIn('Сторінку не знайдено', response_text)
#         self.assertIn('404', response_text)

#     def test_inactive_post_is_hidden(self):
#         """Тест, що неактивні пости не відображаються"""
#         inactive_post = self._create_dummy_post(title="Inactive Post", is_active=False)
        
#         response_list = self.client.get('/post/')
#         self.assertEqual(response_list.status_code, 200)
#         self.assertNotIn(b"Inactive Post", response_list.data)
        
#         response_detail = self.client.get(f'/post/{inactive_post.id}')
#         self.assertEqual(response_detail.status_code, 404)

# if __name__ == '__main__':
#     unittest.main()