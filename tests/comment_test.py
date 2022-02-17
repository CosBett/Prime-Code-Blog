import unittest
from app.models import Comment, Blog, User
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        
        self.new_comment = Comment(id = 1, comment = 'Coment to be test', user = self.user_Mandellah, blog_id = self.new_blog)
        
    def tearDown(self):
        Blog.query.delete()
        User.query.delete()
    
    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Coment to be test')
        self.assertEquals(self.new_comment.user,self.user_Mandellah)
        self.assertEquals(self.new_comment.blog_id,self.new_blog)


class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Mandellah = User(username='Mandellah', password='poi2134', email='mandellah94@gmail.com')
        self.new_blog = Blog(id=1, title='Test', content='Blog to be tested', user_id=self.user_Mandellah.id)
        self.new_comment = Comment(id=1, comment ='Comment to be tested', user_id=self.user_Mandellah.id, blog_id = self.new_blog.id )

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment, 'Comment to be tested')
        self.assertEquals(self.new_comment.user_id, self.user_Mandellah.id)
        self.assertEquals(self.new_comment.blog_id, self.new_blog.id)

    def test_save_comment(self):
        self.new_comment.save()
        self.assertTrue(len(Comment.query.all()) > 0)

    def test_get_comment(self):
        self.new_comment.save()
        get_comment = Comment.get_comment(1)
        self.assertTrue(get_comment is not None)