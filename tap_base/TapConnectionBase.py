"""Shared parent class for TapBase, TargetBase, and TransformBase."""

import abc
from typing import Any, List

DEFAULT_QUOTE_CHAR = '"'
OTHER_QUOTE_CHARS = ['"', "[", "]", "`"]


class TapConnectionBase(metaclass=abc.ABCMeta):
    """Abstract base class for tap connections."""

    _config: dict
    _conn: Any

    def __init__(self, config: dict):
        """Initialize connection."""
        self._config = config

    @abc.abstractmethod
    def open_connection(self) -> Any:
        """Initialize the tap connection."""
        pass

    def is_connected(self) -> bool:
        """Return True if connected."""
        return self._conn is not None

    def ensure_connected(self):
        """Connect if not yet connected."""
        if not self.is_connected():
            self.open_connection()

    def enquote(self, identifier: str):
        """Escape identifier to be SQL safe."""
        for quotechar in [DEFAULT_QUOTE_CHAR] + OTHER_QUOTE_CHARS:
            if quotechar in identifier:
                raise Exception(
                    f"Can't escape identifier `{identifier}` because it contains a "
                    f"quote character ({quotechar})."
                )
        return f"{DEFAULT_QUOTE_CHAR}{identifier.upper()}{DEFAULT_QUOTE_CHAR}"

    def dequote(self, identifier: str):
        """Dequote identifier from quoted version."""
        for quotechar in [DEFAULT_QUOTE_CHAR] + OTHER_QUOTE_CHARS:
            if identifier.startswith(quotechar):
                return identifier.lstrip(quotechar).rstrip(quotechar)
