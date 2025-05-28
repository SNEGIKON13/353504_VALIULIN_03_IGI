from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from ..models import CustomUser, Article, Review, Group, Gym
from datetime import timedelta

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            phone="+375 (29) 123-45-67",
            birth_date=timezone.now().date() - timedelta(days=365*20)
        )
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content"
        )

    def test_home_view(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_view(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_reviews_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')

    def test_reviews_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:reviews'), {
            'rating': 5,
            'text': 'Great service!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after post
        self.assertTrue(Review.objects.filter(text='Great service!').exists())

class GroupViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            phone="+375 (29) 123-45-67",
            birth_date=timezone.now().date() - timedelta(days=365*20)
        )
        self.gym = Gym.objects.create(
            name="Test Gym",
            description="Test Description",
            capacity=20
        )
        self.group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            price=100.00,
            duration=60,
            gym=self.gym,
            capacity=10,
            start_date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timedelta(hours=1)).time(),
            repeat_days=7,
            total_sessions=8
        )

    def test_groups_view_requires_login(self):
        response = self.client.get(reverse('main:groups'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_groups_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:groups'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups.html')

    def test_join_group(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:join_group', kwargs={'group_id': self.group.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after join
        self.assertTrue(self.group.members.filter(id=self.user.id).exists())
