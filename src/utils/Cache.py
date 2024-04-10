from typing import Any


class Cache:
    """
    Cache class is used to store the cached data.
    One instance of Cache is shared among all the classes to follow the Singleton design pattern.

    Attributes:
    ----------
    _cache: dict
        A private attribute to store the cached data.

    Methods:
    --------
    add(key: str, value: Any) -> None:
        Add a key-value pair to the cache.

    reset(key: str, value: Any) -> None:
        Reset the value of a key in the cache to another value.

    get(key: str) -> Any:
        Get the value of a key in the cache.

    get_keys() -> list:
        Get all the keys in the cache.

    remove(key: str) -> None:
        remove a key-value pair from the cache.

    clear() -> None:
        Clear the cache.
    """

    _cache: dict = {}
    _instance = None

    def __new__(cls):
        """
        Create a new instance of Cache if it does not exist.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def add(cls, key: str, value: Any) -> None:
        """
        Add a key-value pair to the cache.

        Parameters:
        -----------
        key : str
            The key to be added to the cache.
        value : Any
            The value corresponding to the key.

        Raises:
        -------
        ValueError:
            If the key is already present in the cache.
        """
        if not cls._cache.get(key):
            cls._cache[key] = value
        else:
            raise ValueError(f"{key} already in _cache")

    @property
    def cache(self):
        """
        Get the cache dictionary.
        """
        return self._cache

    @classmethod
    def reset(cls, key: str, value: Any) -> None:
        """
        Reset the value of a key in the cache to another value.

        Parameters:
        -----------
        key : str
            The key whose value is to be reset.
        value : Any
            The new value to be set for the key.
        """
        cls._cache[key] = value

    @classmethod
    def get(cls, key: str) -> Any:
        """
        Get the value of a key in the cache.

        Parameters:
        -----------
        key : str
            The key whose value is to be retrieved.

        Returns:
        --------
        Any:
            The value corresponding to the key, if present.
        """
        return cls._cache.get(key)

    @classmethod
    def get_keys(cls) -> list:
        """
        Get all the keys in the cache.

        Returns:
        --------
        list:
            A list containing all the keys present in the cache.
        """
        return list(cls._cache.keys())

    @classmethod
    def remove(cls, key: str) -> None:
        """
        remove a key-value pair from the cache.

        Parameters:
        -----------
        key : str
            The key to be removed from the cache.
        """
        if key in cls._cache:
            cls._cache.pop(key)

    @classmethod
    def clear(cls) -> None:
        """
        Clear the cache.
        """
        cls._cache.clear()
