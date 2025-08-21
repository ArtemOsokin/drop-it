# pylint: disable=redefined-outer-name
import typing

import pytest
from sqlalchemy.orm import Mapper, Relationship, RelationshipProperty
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.models.base import LAZY_TYPE
from app.models.base import Base as _Base
from tests.db.fixture_values import BaseFixtureValues

_RelationShipsType = typing.Collection[Relationship | RelationshipProperty]


class _MapperTestParams(BaseFixtureValues):
    def get_ids(self) -> typing.Iterable[str]:
        return [str(mapper.class_) for mapper in self._mappers]

    def get_params(self) -> typing.Iterable[Mapper]:
        return self._mappers

    @property
    def _mappers(self) -> list[Mapper]:
        return list(self._get_all_mappers())

    @staticmethod
    def _get_all_mappers() -> typing.Iterable[Mapper]:
        _BaseDbEngineCls = typing.cast(DeclarativeMeta, _Base)  # pylint: disable=invalid-name
        return _BaseDbEngineCls.registry.mappers


@pytest.fixture(**_MapperTestParams().parametrized_kwargs)
def model_relationships_parametrized(request) -> _RelationShipsType:
    mapper: Mapper = request.param

    relationships = typing.cast(_RelationShipsType, mapper.relationships)
    yield relationships


def test_all_models_with_raise_lazy_type(model_relationships_parametrized):
    if not model_relationships_parametrized:
        return
    for relationship in model_relationships_parametrized:
        lazy = getattr(relationship, 'lazy')
        if lazy != LAZY_TYPE:  # pragma: no-cover
            pytest.fail(
                f'error in {model_relationships_parametrized}: '
                f'all relationships must have {LAZY_TYPE=}'
            )
