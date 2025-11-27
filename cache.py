from functools import lru_cache
import hashlib

# кэш в памяти на 100 запросов
@lru_cache(maxsize=100)
def get_cached_result(image_hash: str):
    return None

def generate_image_hash(image_file) -> str:
    content = image_file.file.read()
    image_file.file.seek(0)
    return hashlib.md5(content).hexdigest()
