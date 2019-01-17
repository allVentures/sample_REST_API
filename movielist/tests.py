from random import randint, sample
from faker import Faker
from rest_framework.test import APITestCase, APIRequestFactory
from movielist.models import Movie, Person
from movielist.serializers import MovieSerializer
import json


class MovieTestCase(APITestCase):
    def setUp(self):
        # populate fake persons names
        self.faker = Faker("pl_PL")
        for x in range(8):
            Person.objects.create(name=self.faker.name())
        for x in range(8):
            self.create_fake_movie()

    def random_person(self):
        people = Person.objects.all()
        return people[randint(0, len(people) - 1)]

    def find_person_by_name(self, name):
        return Person.objects.filter(name=name).first()

    def fake_movie_data(self):
        movie_data = {
            "title": "{} {}".format(self.faker.job(), self.faker.first_name()),
            "description": self.faker.sentence(),
            "year": int(self.faker.year()),
            "director": self.random_person().name,
        }
        people = Person.objects.all()
        actors = sample(list(people), randint(1, len(people)))
        actor_names = [a.name for a in actors]
        movie_data["actors"] = actor_names
        return movie_data

    def create_fake_movie(self):
        # Generate fake movies
        movie_data = self.fake_movie_data()
        movie_data["director"] = self.find_person_by_name(
            movie_data["director"])
        actors = movie_data["actors"]
        del movie_data["actors"]
        new_movie = Movie.objects.create(**movie_data)
        for actor in actors:
            new_movie.actors.add(self.find_person_by_name(actor))

    def test_post_movie(self):
        movies_before = Movie.objects.count()
        new_movie = self.fake_movie_data()
        response = self.client.post("/movies/", new_movie, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Movie.objects.count(), movies_before + 1)
        for key, val in new_movie.items():
            self.assertIn(key, response.data)
            if isinstance(val, list):
                # Compare contents regardless of their order
                self.assertCountEqual(response.data[key], val)
            else:
                self.assertEqual(response.data[key], val)

    def test_get_movie_list(self):
        response = self.client.get("/movies/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Movie.objects.count(), len(response.data))

    def test_get_movie_detail(self):
        all_movies = Movie.objects.all()
        for el in all_movies:
            response = self.client.get(
                "/movies/%s/" % el.id, {}, format='json')
        self.assertEqual(response.status_code, 200)
        for field in ["title", "year", "description", "director", "actors"]:
            self.assertIn(field, response.data)

    def test_delete_movie(self):
        all_movies = Movie.objects.all()
        all_movies_count = all_movies.count()
        random_movie = randint(1, all_movies_count)
        random_movie_id = all_movies[random_movie-1].id
        response = self.client.delete(
            "/movies/%s/" % random_movie_id, {}, format='json')
        self.assertEqual(response.status_code, 204)
        movie_ids = [movie.id for movie in Movie.objects.all()]
        self.assertNotIn(random_movie_id, movie_ids)

    def test_update_movie(self):
        all_movies = Movie.objects.all()
        all_movies_count = all_movies.count()
        random_movie = randint(1, all_movies_count)
        random_movie_id = all_movies[random_movie-1].id

        response = self.client.get("/movies/%s/" %
                                   random_movie_id, {}, format='json')
        movie_data = response.data
        new_year = 2007
        movie_data["year"] = new_year
        new_actors = [self.random_person().name]
        movie_data["actors"] = new_actors
        response = self.client.patch(
            "/movies/%s/" % random_movie_id, movie_data, format='json')
        self.assertEqual(response.status_code, 200)
        movie_obj = Movie.objects.get(id=random_movie_id)
        self.assertEqual(movie_obj.year, new_year)
        db_actor_names = [actor.name for actor in movie_obj.actors.all()]
        self.assertCountEqual(db_actor_names, new_actors)

# python3 manage.py test --keepdb
