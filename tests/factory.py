import factory
from factory.base import T
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Drop, Genre
from app.db.models.user import User

faker = Faker()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    async def create(cls, session: AsyncSession = None, commit: bool = False, **kwargs) -> T:
        obj = cls.build(**kwargs)
        if session:
            session.add(obj)
            if commit:
                await session.commit()
            else:
                await session.flush()
        return obj


class UserFactory(BaseFactory):
    class Meta:
        model = User
        abstract = False

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


class GenreFactory(BaseFactory):
    class Meta:
        model = Genre
        abstract = False

    name = factory.LazyAttribute(lambda _: faker.word())
    slug = factory.LazyAttribute(lambda _: faker.word())


class DropFactory(BaseFactory):
    class Meta:
        model = Drop
        abstract = False

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=300))
    file_url = factory.LazyAttribute(lambda _: faker.file_path(extension='mp3'))
    cover_url = factory.LazyAttribute(lambda _: faker.image_url())

    is_archived = False
    is_expired = False

    expires_at = factory.LazyAttribute(lambda _: faker.future_datetime(end_date='+7d'))

    artist = factory.SubFactory(UserFactory)
    genre = factory.SubFactory(GenreFactory)
