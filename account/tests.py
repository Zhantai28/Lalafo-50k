from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

class ProfileModelTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(username='testuser', password='password')
        self.profile = Profile.objects.create(user=self.user)

    def test_string_method_profile(self):
        profile = User.objects.get(id=1)
        user = self.user
        self.assertEqual(profile, user)

    def test_get_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.profile, self.profile)

