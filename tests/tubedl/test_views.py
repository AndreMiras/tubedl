from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_home(self):
        home_url = reverse("home")
        response = self.client.get(home_url)
        assert response.status_code == 200
        assert b"<h3>Online video downloader</h3>" in response.content

    def test_error404(self):
        error404_url = "does_not_exist"
        response = self.client.get(error404_url)
        assert response.status_code == 404
        assert b"<h1>Page Not Found (404)</h1>" in response.content

    def test_error500(self):
        error500_url = reverse("error500")
        response = self.client.get(error500_url)
        assert response.status_code == 500
        assert b"<h1>Server Error (500)</h1>" in response.content
