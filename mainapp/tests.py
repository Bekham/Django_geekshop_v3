from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command


class TestMainappSmoke(TestCase):
    status_code_succsess = 200

    def setUp(self) -> None:
        category = ProductCategory.objects.create(name='Test')
        Product.objects.create(category=category, name='product_test', price=100)
        self.client = Client()


    def test_products_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_succsess)

    def test_products_product(self):
        for item in Product.objects.all():
            response = self.client.get(f'/products/detail/{item.pk}/')
            self.assertEqual(response.status_code, self.status_code_succsess)


    def test_products_basket(self):
        response = self.client.get(f'/users/profile/')
        self.assertEqual(response.status_code, 302)


    def tearDown(self) -> None:
        pass
