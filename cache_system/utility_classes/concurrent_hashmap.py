import threading


class ConcurrentHashMap:
    def __init__(self):
        self._dict = dict()
        self._lock = threading.Lock()
    
    # def __setitem__(self, key, value):
    def set(self, key, value):
        with self._lock:
            self._dict[key] = value
    
    # def __getitem__(self, key):
    def get(self, key):
        with self._lock:
            if key in self._dict: 
                return self._dict[key]
            else:
                raise KeyError(f"Key {key} not found")
    
    # def __delitem__(self, key):
    def delete(self, key):
        with self._lock:
            if key in self._dict: 
                del self._dict[key]
            else:
                raise KeyError(f"Key {key} not found")
    
    
    def contains_key(self, key):
        with self._lock:
            return key in self._dict
    
    def size(self):
        with self._lock:
            return len(self._dict)
    
    

    