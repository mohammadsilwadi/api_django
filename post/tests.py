from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snack

class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Snack.objects.create(
            purchaser = test_user,
            title = 'Title of Blog',
            description = 'Words about the blog'
        )
        test_post.save()

    def test_blog_content(self):
        post = Snack.objects.get(id=1)

        self.assertEqual(str(post.purchaser), 'tester')
        self.assertEqual(post.title, 'Title of Blog')
        self.assertEqual(post.description, 'Words about the blog')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Snack.objects.create(
            purchaser = test_user,
            title = 'Title of Blog',
            description = 'Words'
        )
        test_post.save()

        response = self.client.get(reverse('posts_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_post.title,
            'description': test_post.description,
            'purchaser': test_user.username,
            
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('posts_list')
        data = {
            "title":"Testing is Fun!!!",
            "description":"when the right tools are available",
            "purchaser":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Snack.objects.count(), 1)
        self.assertEqual(Snack.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Snack.objects.create(
            purchaser = test_user,
            title = 'Title of Blog',
            description = 'Words about the blog'
        )

        test_post.save()

        url = reverse('posts_detail',args=[test_post.id])
        data = {
            "title":"Testing is Still Fun!!!",
            "purchaser":test_post.purchaser.id,
            "description":test_post.description,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Snack.objects.count(), test_post.id)
        self.assertEqual(Snack.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a post."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Snack.objects.create(
            purchaser = test_user,
            title = 'Title of Blog',
            description = 'Words about the blog'
        )

        test_post.save()

        post = Snack.objects.get()

        url = reverse('posts_detail', kwargs={'pk': post.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)

# Create your tests here.
