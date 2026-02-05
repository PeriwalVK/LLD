from multiprocessing import dummy


class DLLNode:
    def __init__(self, key, prev=None, next=None):
        self.key = key
        # self.val = val
        self.next: DLLNode = None
        self.prev: DLLNode = None


class DLL:
    def __init__(self):
        self.dummy_head = DLLNode(None)
        self.dummy_tail = DLLNode(None)

        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head

    def get_head(self) -> DLLNode:
        if self.dummy_head.next is self.dummy_tail:
            return None
        return self.dummy_head.next

    def _detach(self, node: DLLNode):
        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev, node.next = None, None

    def _attach_to_tail(self, node: DLLNode):
        dummy_tail_prev = self.dummy_tail.prev
        dummy_tail_prev.next = self.dummy_tail.prev = node

        node.prev, node.next = dummy_tail_prev, self.dummy_tail

    def insert_new_to_tail(self, key) -> DLLNode:
        new_node = DLLNode(key)
        self._attach_to_tail(new_node)
        return new_node

    def move_to_tail(self, node: DLLNode):
        self._detach(node)
        self._attach_to_tail(node)

    def delete_head(self) -> None:
        head = self.get_head()
        if head:
            self._detach(head)
            del head
        # else:
        #     # raise Exception("Nothing in LRU to evict")
    
    def __str__(self):
        res = []
        node = self.dummy_head.next
        while node is not self.dummy_tail:
            res.append(node.key)
            node = node.next
        return "->".join([str(x) for x in res])
