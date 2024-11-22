import time
import numpy as np
from statistics import mean, stdev
from functools import wraps

class LongTimeDecorator:
    def __init__(self):
        self.times = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_time = time.perf_counter() - start_time
            self.times.append(elapsed_time)
            return result
        return wrapper

    def stats(self):
        if not self.times:
            return "Nie ma żadnych czasów do analizy."
        return {
            "count": len(self.times),
            "average": round(mean(self.times), 3),
            "min": round(min(self.times), 3),
            "max": round(max(self.times), 3),
            "stdev": round(stdev(self.times), 3),
        }

long_time = LongTimeDecorator()

@long_time
def long_time_function():
    np.random.seed(42)
    matrix = np.random.rand(1500, 1500)
    return np.linalg.svd(matrix)

for _ in range(10):
    long_time_function()

print("Statystyki czasów wykonania:")
print(long_time.stats())
