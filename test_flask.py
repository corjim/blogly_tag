from unittest import TestCase

from app import app
from models import db, Blog, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_user_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


db.drop_all()
db.create_all()

# test for blogger/user route

class BlogViewsTestCase(TestCase):
    """Tests for views for Blogs."""

    def setUp(self):
        """Add sample user"""

        Blog.query.delete()

        user = Blog(first_name="Testuser", last_name="blogger", image_url='https://www.theresnophoto.com')
        db.session.add(user)
        db.session.commit()

        self.bloggers_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testuser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.bloggers_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestPet</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser", "last_name": "blogger"}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestUser</h1>", html)



#   test for post routes

class PostViewsTestCase(TestCase):
    """Tests for views for Blogs."""

    def setUp(self):
        """Add sample blog post"""

        Post.query.delete()

        post = Post(title="Testpost", content="TestContent")
        db.session.add(post)
        db.session.commit()

        self.posts_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testpost', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.posts_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestPost</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            p = {"title": "TestPost", "content": "post content"}
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPost</h1>", html)


