from abc import ABC, abstractmethod
import threading
from typing import Any, Dict, override

from cache_system.utility_classes.dll import DLL, DLLNode


class IEvictionPolicy(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def evict(self, key):
        """returns key of the evicted node"""
        pass

    @abstractmethod
    def mark_key_accessed(self, key):
        pass


class LRUEvictionPolicy(IEvictionPolicy):
    @override
    def __init__(self):
        # self.capacity = capacity
        self.dll = DLL()
        self.key_node_map: Dict[Any, DLLNode] = dict()

        self._lock = threading.Lock()


    @override
    def evict(self):
        with self._lock:
            
            head = self.dll.get_head()
            if head:

                key = head.key
                self.key_node_map.pop(key)
                self.dll.delete_head()
                
                prefix = f"[{threading.current_thread().name}-evictkey={key}]"
                print(f"{prefix}: LRU is now {self.dll}")
                return key
            else:
                # raise Exception("Nothing in LRU to evict")
                prefix = f"[{threading.current_thread().name}]"
                print(f"{prefix}: Nothing evicted, LRU is now {self.dll}")
                return None
            
            
    @override
    def mark_key_accessed(self, key):
        with self._lock:
            if key in self.key_node_map:
                node = self.key_node_map[key]
                self.dll.move_to_tail(node)
            else:
                new_node = self.dll.insert_new_to_tail(key)
                self.key_node_map[key] = new_node
            prefix = f"[{threading.current_thread().name}-key={key}]"
            print(f"{prefix}: marked key access - LRU is now {self.dll}")
