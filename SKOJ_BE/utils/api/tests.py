from django.urls import reverse
from django.test.testcases import TestCase
from rest_framework.test import APIClient

from account.models import AdminType, Permission, User, UserProfile


class APITestCase(TestCase):
    client_class = APIClient

    def create_user(self, username, password, admin_type=AdminType.REGULAR_USER, login=True,
                    problem_permission=Permission.NONE, course_permission=Permission.NONE):
        user = User.objects.create(username=username, admin_type=admin_type, problem_permission=problem_permission, course_permission=course_permission)
        user.set_password(password)
        UserProfile.objects.create(user=user)
        user.save()
        if login:
            self.client.login(username=username, password=password)
        return user

    def create_admin(self, username="admin", password="admin", login=True):
        return self.create_user(username=username, password=password, admin_type=AdminType.ADMIN,
                                problem_permission=Permission.OWN, coure_permission=Permission.OWN,
                                login=login)

    def create_super_admin(self, username="root", password="root", login=True):
        return self.create_user(username=username, password=password, admin_type=AdminType.SUPER_ADMIN,
                                problem_permission=Permission.ALL, course_permission = Permission.ALL, login=login)

    def reverse(self, url_name, *args, **kwargs):
        return reverse(url_name, *args, **kwargs)

    def assertSuccess(self, response):
        if not response.data["error"] is None:
            raise AssertionError("response with errors, response: " + str(response.data))

    def assertFailed(self, response, msg=None):
        self.assertTrue(response.data["error"] is not None)
        if msg:
            self.assertEqual(response.data["data"], msg)
