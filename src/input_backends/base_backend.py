from abc import ABC, abstractmethod
from core.input_state import InputState

class BaseInputBackend(ABC):
    """
    Abstract Base Class for all hardware input backends.
    Ensures that every backend returns a unified InputState object.
    """
    def __init__(self):
        self.state = InputState()

    @abstractmethod
    def start(self):
        """Initialize and start the hardware listener."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the hardware listener and cleanup."""
        pass

    @abstractmethod
    def poll(self):
        """Return the current InputState."""
        return self.state
