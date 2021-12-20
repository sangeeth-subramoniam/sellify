from django.test import TestCase


from django.contrib.auth.models import User
from registration.models import user_profile


class RegistrationTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="testuser", sound="testpass")

        login = self.client.login(username='testuser', password='testpass')
        print(login)