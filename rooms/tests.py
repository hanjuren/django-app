from rest_framework.test import APITestCase
from . import models


class TsetAmenitiees(APITestCase):

    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity test"
    DESC = "Amenity test description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, list, "Response data isn't List.")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], self.NAME)
        self.assertEqual(data[0]['description'], self.DESC)

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity description"

        response = self.client.post(
            self.URL,
            data={"name": new_amenity_name, "description": new_amenity_desc},
        )
        data = response.json()

        self.assertEqual(response.status_code, 201, "Not 201 status code")
        self.assertEqual(data['name'], new_amenity_name)
        self.assertEqual(data['description'], new_amenity_desc)

    def test_create_amenity_vaild_error(self):
        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertIn('name', data)


class TestAmenity(APITestCase):

    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity test"
    DESC = "Amenity description"

    def setUp(self):
        self.amenity = models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_get_amenity(self):
        response = self.client.get(f"{self.URL}{self.amenity.pk}/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['pk'], self.amenity.pk)
        self.assertEqual(data['name'], self.amenity.name)
        self.assertEqual(data['description'], self.amenity.description)
