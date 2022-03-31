from abc import ABCMeta, abstractmethod, abstractproperty

# Abstract base class for all the different types of input
class GenericInput(metaclass=ABCMeta):
    # __metaclass__ = ABCMeta
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def get_bytes(self):
        pass

    @abstractmethod
    def close(self):
        pass
