from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from ..models import CustomUser, Group, Gym, Review
from datetime import datetime, timedelta

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser",
            phone="+375 (29) 123-45-67",
            birth_date=timezone.now().date() - timedelta(days=365*20)  # 20 years old
        )

    def test_is_adult(self):
        self.assertTrue(self.user.is_adult())
        
    def test_phone_validation(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                username="badphone",
                phone="123456",  # Invalid format
                birth_date=timezone.now().date()
            )
            user.full_clean()

class GroupTests(TestCase):
    def setUp(self):
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

    def test_available_spots(self):
        self.assertEqual(self.group.available_spots, 10)

    def test_schedule_dates(self):
        dates = self.group.get_schedule_dates()
        self.assertIsInstance(dates, list)
        self.assertLessEqual(len(dates), self.group.total_sessions)

class ReviewTests(TestCase):
    def setUp(self):
        self.review = Review.objects.create(
            name="Test User",
            rating=5,
            text="Great service!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.text, "Great service!")

    def test_str_representation(self):
        self.assertEqual(str(self.review), "Test User - 5★")

    def test_invalid_rating(self):
        with self.assertRaises(ValidationError):
            review = Review(
                name="Test User",
                rating=6,  # Invalid rating
                text="Test"
            )
            review.full_clean()
