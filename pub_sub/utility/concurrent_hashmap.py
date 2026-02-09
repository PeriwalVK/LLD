import threading
from typing import Dict



class ConcurrentHashMap[U,V]:
    def __init__(self):
        self._dict: Dict[U,V] = dict()
        self._lock = threading.Lock()
    
    # def __setitem__(self, key, value):
    def set(self, key: U, value: V):
        with self._lock:
            self._dict[key] = value
    
    # def __getitem__(self, key):
    def get(self, key: U) -> V:
        with self._lock:
            if key in self._dict: 
                return self._dict[key]
            else:
                raise KeyError(f"Key {key} not found")
    
    # def __delitem__(self, key):
    def delete(self, key: U):
        with self._lock:
            if key in self._dict: 
                del self._dict[key]
            else:
                raise KeyError(f"Key {key} not found")
    
    
    def contains_key(self, key: U) -> bool:
        with self._lock:
            return key in self._dict
    
    def size(self) -> int:
        with self._lock:
            return len(self._dict)
    
    

    