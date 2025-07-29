import factory
from faker import Faker

from app.db import models

faker = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None

    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    hashed_password = factory.LazyAttribute(lambda _: "$2b$12$mockedhashedpassword")
    is_artist = factory.LazyAttribute(lambda _: faker.boolean())
    birthday = factory.LazyAttribute(lambda _: faker.date_of_birth(minimum_age=18, maximum_age=30))
    avatar_url = factory.LazyAttribute(lambda _: faker.image_url())
    is_active = True
    is_admin = False
    is_verified = factory.LazyAttribute(lambda _: faker.boolean())
    last_login = factory.LazyAttribute(
        lambda _: faker.date_time_this_year(before_now=True, after_now=False)
    )
