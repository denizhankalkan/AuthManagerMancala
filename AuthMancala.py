class Node:
    def __init__(self, value, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.value = value

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        new_node = Node(value=value, prev=self.tail)        
        
        if self.head is None:
            self.head = new_node
        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node

        self.size += 1
        return new_node
    
    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next
        if self.tail == node:
            self.tail = node.prev
        self.size -= 1

    def get_size(self):
        return self.size

class AuthenticationManager:
    def __init__(self, timeToLive: int):
        self.ttl = timeToLive
        self.token_map = {}
        self.token_list = DoublyLinkedList()
    
    def enable_inplace_cleanups():
        self.inplace_cleanups = True
    
    def _remove(self, tokenId: str):
        token_node = self.token_map.get(tokenId)
        if token_node:
            del self.token_map[tokenId]
            self.token_list.remove(token_node)
        return token_node

    def _cleanup(self, currentTime: int, limit: int = float("+inf")) -> None:
        while self.token_list.head and limit > 0:
            (tokenId, expirationTime) = self.token_list.head.value
            if expirationTime <= currentTime:
                self._remove(tokenId)
                limit -= 1
            else:
                break

    def generate(self, tokenId: str, currentTime: int) -> None:
        if self.inplace_cleanups:
            self._cleanup(currentTime, limit=1)
        newExpirationTime = currentTime + self.ttl
        self.token_map[tokenId] = self.token_list.append((tokenId, newExpirationTime))

    def renew(self, tokenId: str, currentTime: int) -> None:
        if self.inplace_cleanups:
            self._cleanup(currentTime, limit=1)
        token_node = self._remove(tokenId)
        if token_node:
            expirationTime = token_node.value[1]
            if expirationTime > currentTime:
                self.generate(tokenId, currentTime)

    def countUnexpiredTokens(self, currentTime: int) -> int:
        self._cleanup(currentTime)
        return self.token_list.get_size()
