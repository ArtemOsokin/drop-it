from pydantic import BaseModel, HttpUrl

from app.utils.patch import apply_schema


class DummyModel:
    def __init__(self, name: str = "init", age: int = 0, url: str | None = None):
        self.name = name
        self.age = age
        self.url = url


def test_apply_schema_updates_fields(faker):
    class Schema(BaseModel):
        name: str
        age: int

    model = DummyModel()
    fake_name = faker.first_name()
    schema = Schema(name=fake_name, age=30)

    updated = apply_schema(model, schema)

    assert updated.name == fake_name
    assert updated.age == 30


def test_apply_schema_excludes_unset_fields(faker):
    class Schema(BaseModel):
        name: str | None = None
        age: int | None = None

    fake_age = faker.pyint(min_value=5, max_value=100)
    fake_new_name = faker.word()

    model = DummyModel(name="keep", age=fake_age)
    schema = Schema(name=fake_new_name)

    updated = apply_schema(model, schema)

    assert updated.name == fake_new_name
    assert updated.age == fake_age


def test_apply_schema_respects_allowed_fields(faker):
    class Schema(BaseModel):
        name: str
        age: int

    fake_old_age = faker.pyint(min_value=5, max_value=100)
    fake_new_name = faker.word()

    model = DummyModel(name="old", age=fake_old_age)
    schema = Schema(name=fake_new_name, age=fake_old_age + 1)

    updated = apply_schema(model, schema, allowed_fields=["name"])

    assert updated.name == fake_new_name
    assert updated.age == fake_old_age  # не изменилось


def test_apply_schema_converts_httpurl_to_str(faker):
    class Schema(BaseModel):
        url: HttpUrl

    fake_url = faker.url()

    model = DummyModel(url=None)
    schema = Schema(url=fake_url)

    updated = apply_schema(model, schema)

    assert isinstance(updated.url, str)
    assert updated.url == fake_url


def test_apply_schema_ignores_unknown_fields(faker):
    class Schema(BaseModel):
        temp1: str | None = None
        temp2: int | None = None

    fake_old_age = faker.pyint(min_value=5, max_value=100)
    fake_keep_name = faker.word()

    model = DummyModel(name=fake_keep_name, age=fake_old_age)
    schema = Schema(temp1="hello", temp2=fake_old_age + 1)

    updated = apply_schema(model, schema)

    assert updated.name == fake_keep_name
    assert updated.age == fake_old_age
    assert not hasattr(updated, "temp1")
    assert not hasattr(updated, "temp2")
