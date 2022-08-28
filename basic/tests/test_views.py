# from django.test import RequestFactory
# from django.urls import reverse
# from mixer.backend.django import mixer
# from django.contrib.auth.models import User, AnonymousUser
#
# from basic.views import Profile
# import pytest
#
#
# @pytest.mark.django_db
# class TestViews:
#
#     def setUpClass(cls):
#         super(TestViews, cls).setUpClass()
#         mixer.blend('basic.models.User')
#         cls.factory = RequestFactory()
#
#     def test_profile_authenticated(self):
#         # mixer.blend('django.contrib.auth.models.User')
#         # mixer.blend('basic.models.User')
#         path = reverse('Profile', kwargs={'pk': 1})
#         # request = RequestFactory().get(path)
#         request = self.factory.get(path)
#         request.user = mixer.blend('User')
#
#         response = Profile.get(request, pk=1)
#         assert response.status_code == 200
#
#     def test_profile_unauthenticated(self):
#         # mixer.blend('django.contrib.auth.models.User')
#         path = reverse('Profile', kwargs={'pk': 1})
#         # request = RequestFactory().get(path)
#         request = self.factory.get(path)
#         request.user = AnonymousUser()
#
#         response = Profile.get(request, pk=1)
#         assert 'profile/' in response.url
