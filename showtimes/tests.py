from faker import Faker
from random import randint
from rest_framework.test import APITestCase, APIRequestFactory
from showtimes.models import Cinema, Screening
from movielist.models import Movie
from showtimes.serializers import CinemaSerializer


class CinemaTestCase(APITestCase):

    def setUp(self):
        # populate random cinemas data
        self.faker = Faker("pl_PL")
        for i in range(1, 6):
            Cinema.objects.create(name=self.faker.name(),
                                  city=self.faker.city())

    def test_get_cinema_list(self):
        response = self.client.get("/cinemas/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.count(), len(response.data))

    def test_get_cinema_detail(self):
        all_cinemas = Cinema.objects.all()
        all_cinemas_count = all_cinemas.count()
        random_cinema = randint(1, all_cinemas_count)
        random_cinema_id = all_cinemas[random_cinema-1].id
        response = self.client.get("/cinemas/%s/" %
                                   random_cinema_id, {}, format='json')
        self.assertEqual(response.status_code, 200)
        for field in ["city", "name"]:
            self.assertIn(field, response.data)
