import random
import time
from collections import OrderedDict


class LRUCache:
    """Реалізація LRU-кеша з фіксованим розміром."""

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        """Отримує значення з кешу, якщо воно існує."""
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # Оновлюємо порядок використання
        return self.cache[key]

    def put(self, key, value):
        """Додає новий елемент у кеш, видаляючи застарілий у разі необхідності."""
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Видалення найменш використовуваного елемента
        self.cache[key] = value

    def invalidate(self, index):
        """Видаляє записи з кешу, які стали неактуальними після оновлення масиву."""
        keys_to_delete = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_delete:
            del self.cache[key]


# Функції без кешування

def range_sum_no_cache(array, L, R):
    """Обчислює суму елементів у вказаному діапазоні без кешування."""
    return sum(array[L:R + 1])


def update_no_cache(array, index, value):
    """Оновлює значення елемента масиву за заданим індексом без використання кешу."""
    array[index] = value


# Ініціалізація кешу
cache = LRUCache(1000)


def range_sum_with_cache(array, L, R):
    """Повертає суму діапазону з використанням кешу, запобігаючи повторним обчисленням."""
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    """Оновлює значення у масиві та очищує кеш для відповідних діапазонів."""
    array[index] = value
    cache.invalidate(index)


# Генерація тестових даних
N = 100_000
Q = 50_000
array = [random.randint(1, 1000) for _ in range(N)]
queries = []
for _ in range(Q):
    if random.random() < 0.7:  # 70% ймовірність запиту Range, 30% Update
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(("Range", L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(("Update", index, value))

# Вимірювання часу виконання без кешування
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
time_no_cache = time.time() - start_time

# Перезапуск кешу перед тестуванням з кешуванням
cache = LRUCache(1000)
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(array, query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
time_with_cache = time.time() - start_time

# Вивід результатів
print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")
