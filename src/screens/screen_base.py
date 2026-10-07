from abc import ABC, abstractmethod


class ScreenBase(ABC):
    @abstractmethod
    def event_cacher(self) -> None:
        ...

    @abstractmethod
    def change_screen(self) -> str:
        ...

    @abstractmethod
    def render(self) -> None:
        ...

    @abstractmethod
    def clear_screen(self) -> None:
        ...
