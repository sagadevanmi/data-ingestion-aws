from abc import ABC, abstractmethod


class BaseConnector(ABC):
    @abstractmethod
    def read(self, **kwargs):
        """"""
        pass
