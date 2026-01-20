class DynamicArray:
    def __init__(self):
        self._capacity = 4
        self._size = 0
        self._data = [None] * self._capacity

    def append(self, item):
        # check if resized needed
        if self._size + 1 > self._capacity:
            self._resize(2 * self._capacity)

        # put item at next free index
        self._data[self._size] = item
        # and increment array size
        self._size += 1

    def get(self, index):
        if index >= self._size:
            raise IndexError
        return self._data[index]

    def set(self, index, item):
        if index >= self._size:
            raise IndexError
        self._data[index] = item

    def insert(self, index, item):
        if self._size + 1 > self._capacity:
            self._resize(2 * self._capacity)

        # shift elements at index to the right
        # going right-to-left
        for i in range(self._size - 1, index - 1, -1):
            self._data[i+1] = self._data[i]

        # allocate the next element
        self._size += 1

        self._data[index] = item

    def delete(self, index):
        if index >= self._size:
            raise IndexError

        # delete at index by left shifting everything to its right
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._size -= 1

    def size(self):
        return self._size

    def _resize(self, new_capacity):
        assert new_capacity > self._capacity
        self._data = self._data[:] + [None] * (new_capacity - self._size)
        self._capacity = new_capacity


def test_dynamic_array():
    # Basic append and get
    arr = DynamicArray()
    arr.append(1)
    arr.append(2)
    arr.append(3)
    assert arr.get(0) == 1
    assert arr.get(1) == 2
    assert arr.get(2) == 3
    assert arr.size() == 3

    # Set
    arr.set(1, 99)
    assert arr.get(1) == 99

    # Resize on append
    arr.append(4)
    arr.append(5)  # Should trigger resize past capacity 4
    assert arr.size() == 5
    assert arr.get(4) == 5

    # Insert at beginning
    arr.insert(0, 100)
    assert arr.get(0) == 100
    assert arr.get(1) == 1
    assert arr.size() == 6

    # Insert in middle
    arr.insert(3, 200)
    assert arr.get(3) == 200
    assert arr.size() == 7

    print(arr._data)

    # Delete from middle
    arr.delete(3)
    assert arr.get(3) == 3
    assert arr.size() == 6

    # Delete from beginning
    arr.delete(0)
    assert arr.get(0) == 1
    assert arr.size() == 5

    # Delete from end
    arr.delete(arr.size() - 1)
    assert arr.size() == 4

    # Out of bounds
    try:
        arr.get(100)
        assert False, "Should have raised IndexError"
    except IndexError:
        pass

    try:
        arr.set(100, 1)
        assert False, "Should have raised IndexError"
    except IndexError:
        pass

    print("All tests passed!")


if __name__ == '__main__':
    test_dynamic_array()
