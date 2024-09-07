from abc import ABC, abstractmethod


class Handler(ABC):

    @abstractmethod
    def __init__(self):
        pass