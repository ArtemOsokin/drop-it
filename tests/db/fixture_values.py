import abc
import typing


class BaseFixtureValues(abc.ABC):
    @property
    def parametrized_kwargs(self) -> dict:
        return {
            'params': self.get_params(),
            'ids': self.get_ids(),
        }

    @abc.abstractmethod
    def get_params(self) -> typing.Iterable[typing.Any]: ...

    @abc.abstractmethod
    def get_ids(self) -> typing.Iterable[str]: ...
