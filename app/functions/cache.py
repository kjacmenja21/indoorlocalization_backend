import asyncio
from typing import Generic, List, TypeVar

# Define a type variable to allow flexible cache element types
T = TypeVar("T")


class AsyncCache(Generic[T]):
    def __init__(self, max_age: int = 10):
        self.cache: List[T] = []  # List to hold cached elements
        self.max_age = max_age  # Time after which the cache should be cleared
        self._clear_task = None

    async def add(self, item: T):
        """Add an item to the cache."""
        self.cache.append(item)
        # Optionally, set the cache to clear after max_age seconds
        if self._clear_task is None or self._clear_task.done():
            self._clear_task = asyncio.create_task(
                self._clear_cache_after(self.max_age)
            )

    async def _clear_cache_after(self, delay: int):
        """Clear the cache after a certain delay (simulating cache expiration)."""
        await asyncio.sleep(delay)  # Wait for the specified time
        self.cache.clear()  # Clear the cache
        print("Cache cleared")

    def get_cache(self) -> List[T]:
        """Return the current cache."""
        return self.cache

    async def clear_cache(self):
        """Clear the cache explicitly."""
        self.cache.clear()
        print("Cache cleared manually")
