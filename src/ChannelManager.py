class ChannelKeySet:
    def __init__(self, history_len):
        self.data = {}
        self.counter = 0
        self.HISTORY_LEN = history_len

    def add_key(self, key, tup_float):
        """Add a key with the global counter as the first value in the tuple and the provided float_value as the second."""
        self.data[key] = (self.counter, tup_float)
        self.cull_keys()

    def increment_counter(self):
        """Increment the global counter and cull keys if necessary."""
        self.counter += 1
        self.cull_keys()

    def cull_keys(self):
        """Remove keys where the first value of the tuple is less than the global counter minus HISTORY_LEN."""
        to_cull = [key for key, (counter, _) in self.data.items() if counter < self.counter - self.HISTORY_LEN]
        for key in to_cull:
            del self.data[key]

    def __iter__(self):
        """Provide an iterator over the keys, yielding each key's associated tuple."""
        for key in self.data:
            yield key, self.data[key]