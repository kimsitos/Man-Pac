from abc import ABC, abstractmethod


class ScreenBase(ABC):
    @abstractmethod
    def event_cacher():
        ...

    @abstractmethod
    def change_screen() -> str:
        ...

    @abstractmethod
    def render() -> None:
        ...

    @abstractmethod
    def clear_screen() -> None:
        ...
