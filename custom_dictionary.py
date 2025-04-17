class FastCustomDict:
    _LOAD_FACTOR = 0.75

    def __init__(self, initial_capacity=8):
        self.capacity = initial_capacity
        self.size = 0
        self._keys = [None] * self.capacity
        self._values = [None] * self.capacity
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def _resize(self):
        old_keys = self._keys
        old_values = self._values
        self.capacity *= 2
        self.size = 0
        self._keys = [None] * self.capacity
        self._values = [None] * self.capacity

        for k, v in zip(old_keys, old_values):
            if k is not None:
                self[k] = v
    
    def __setitem__(self, key, value):
        if self.size / self.capacity >= self._LOAD_FACTOR:
            self._resize()
        
        idx = self._hash(key)
        while self._keys[idx] is not None and self._keys[idx] != key:
            idx = (idx + 1) % self.capacity
        
        if self._keys[idx] is None:
            self.size += 1

        self._keys[idx] = key
        self._values[idx] = value

    def __getitem__(self, key):
        idx = self._hash(key)
        start_idx = idx
        while self._keys[idx] is not None:
            if self._keys[idx] == key:
                return self._values[idx]
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break
        raise KeyError(key)
    
    def __delitem__(self, key):
        idx = self._hash(key)
        start_idx = idx
        while self._keys[idx] is not None:
            if self._keys[idx] == key:
                self._keys[idx] = None
                self._values[idx] = None
                self.size -= 1
                self._rehash_from(idx)
                return
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break
        raise KeyError(key)
    
    def _rehash_from(self, deleted_index):
        idx = (deleted_index + 1) % self.capacity
        while self._keys[idx] is not None:
            key_to_rehash = self._keys[idx]
            value_to_rehash = self._values[idx]
            self._keys[idx] = None
            self._values[idx] = None
            self.size -= 1
            self[key_to_rehash] = value_to_rehash
            idx = (idx + 1) % self.capacity

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except KeyError:
            return False
    
    def __iter__(self):
        return (k for k in self._keys if k is not None)
    
    def __len__(self):
        return self.size
    
    def __repr__(self):
        return "{" + ", ".join(f"{k}: {v}" for k, v in zip(self._keys, self._values) if k is not None) + "}"
    
    def keys(self):
        return (k for k in self._keys if k is not None)
    
    def values(self):
        return (v for v in self._values if v is not None)
    

dct = FastCustomDict()
dct["a"] = 1
dct["b"] = 2
dct["c"] = 3

print(dct)
print(dct["a"])
print(dct["b"])

print(list(dct.values()))
print(list(dct.keys()))
print(len(dct))
print("a" in dct)
print("z" in dct)

del dct["b"]

print(dct)
print(len(dct))
print("b" in dct)
