

from unittest import TestCase

from app import app
from models import db, Blog, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_user_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

# TESTING FOR BLOG MODELS

class BlogModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""

        Blog.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        pet = Blog(first_name="TestBlog", last_name="blogger")
        self.assertEquals(pet.full_name(), "TestBlog blogger")




#   TESTING FOR POST MODELS

class PostModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""

        Post.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

   

    def test_add_user(self):
        with app.test_client() as client:
             d = {"title": "TestPost", "content": "PostModels"}
             resp = client.post("/", data=d, follow_redirects=True)
             html = resp.get_data(as_text=True)

             self.assertEqual(resp.status_code, 200)
             self.assertIn("<div>TestPost</div>", html)