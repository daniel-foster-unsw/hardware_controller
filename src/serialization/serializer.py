"""
Serializer interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class Serializer(ABC):
    """Base serializer."""

    @abstractmethod
    def serialize(
        self,
        obj: Any,
    ) -> dict:
        """
        Convert an object into a dictionary.
        """

    @abstractmethod
    def deserialize(
        self,
        data: dict,
    ) -> Any:
        """
        Convert a dictionary into an object.
        """