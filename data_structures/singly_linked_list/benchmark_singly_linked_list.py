import time
import matplotlib.pyplot as plt
from singly_linked_list import SinglyLinkedList


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def benchmark_prepend():
    print("Benchmarking prepend...")
    sizes = [1000, 2000, 4000, 8000, 16000, 32000]
    times = []

    for size in sizes:
        ll = SinglyLinkedList()
        total_time = 0

        for i in range(size):
            elapsed, _ = time_operation(ll.prepend, i)
            total_time += elapsed

        avg_time = total_time / size
        times.append(avg_time * 1000000)  # Convert to microseconds
        print(f"Size {size}: {avg_time * 1000000:.2f} μs per prepend")

    return sizes, times


def benchmark_append():
    print("\nBenchmarking append...")
    sizes = [1000, 2000, 3000, 4000, 5000]
    times = []

    for size in sizes:
        ll = SinglyLinkedList()
        total_time = 0

        for i in range(size):
            elapsed, _ = time_operation(ll.append, i)
            total_time += elapsed

        avg_time = total_time / size
        times.append(avg_time * 1000000)
        print(f"Size {size}: {avg_time * 1000000:.2f} μs per append")

    return sizes, times


def benchmark_get():
    print("\nBenchmarking get (worst case - last element)...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    times = []

    for size in sizes:
        ll = SinglyLinkedList()
        for i in range(size):
            ll.prepend(i)

        # Get last element (worst case)
        elapsed, _ = time_operation(ll.get, size - 1)
        times.append(elapsed * 1000000)
        print(f"Size {size}: {elapsed * 1000000:.2f} μs to get last element")

    return sizes, times


def benchmark_insert_middle():
    print("\nBenchmarking insert at middle...")
    sizes = [1000, 2000, 3000, 4000, 5000]
    times = []

    for size in sizes:
        ll = SinglyLinkedList()
        for i in range(size):
            ll.prepend(i)

        # Insert at middle position
        middle = size // 2
        elapsed, _ = time_operation(ll.insert, middle, 999)
        times.append(elapsed * 1000000)
        print(f"Size {size}: {elapsed * 1000000:.2f} μs to insert at middle")

    return sizes, times


def benchmark_delete_middle():
    print("\nBenchmarking delete from middle...")
    sizes = [1000, 2000, 3000, 4000, 5000]
    times = []

    for size in sizes:
        ll = SinglyLinkedList()
        for i in range(size):
            ll.prepend(i)

        # Delete from middle position
        middle = size // 2
        elapsed, _ = time_operation(ll.delete, middle)
        times.append(elapsed * 1000000)
        print(f"Size {size}: {elapsed * 1000000:.2f} μs to delete from middle")

    return sizes, times


def benchmark_find():
    print("\nBenchmarking find (worst case - last element)...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    times = []

    for size in sizes:
        ll = SinglyLinkedList()
        for i in range(size):
            ll.prepend(i)

        # Find element that's at the end (worst case)
        target = size - 1  # This will be the last element added (first in list)
        elapsed, _ = time_operation(ll.find, 0)  # 0 was added first, so it's at the end
        times.append(elapsed * 1000000)
        print(f"Size {size}: {elapsed * 1000000:.2f} μs to find last element")

    return sizes, times


def plot_results():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(14, 12))

    # Prepend - should be O(1)
    sizes, times = benchmark_prepend()
    ax1.plot(sizes, times, 'b-o')
    ax1.set_title('Prepend Performance (Should be O(1))')
    ax1.set_xlabel('List Size')
    ax1.set_ylabel('Time per prepend (μs)')
    ax1.grid(True)

    # Append - should be O(n)
    sizes, times = benchmark_append()
    ax2.plot(sizes, times, 'r-o')
    ax2.set_title('Append Performance (Should be O(n) per operation)')
    ax2.set_xlabel('List Size')
    ax2.set_ylabel('Time per append (μs)')
    ax2.grid(True)

    # Get - should be O(n)
    sizes, times = benchmark_get()
    ax3.plot(sizes, times, 'g-o')
    ax3.set_title('Get Last Element (Should be O(n))')
    ax3.set_xlabel('List Size')
    ax3.set_ylabel('Time to get (μs)')
    ax3.grid(True)

    # Insert middle - should be O(n)
    sizes, times = benchmark_insert_middle()
    ax4.plot(sizes, times, 'm-o')
    ax4.set_title('Insert at Middle (Should be O(n))')
    ax4.set_xlabel('List Size')
    ax4.set_ylabel('Time to insert (μs)')
    ax4.grid(True)

    # Delete middle - should be O(n)
    sizes, times = benchmark_delete_middle()
    ax5.plot(sizes, times, 'c-o')
    ax5.set_title('Delete from Middle (Should be O(n))')
    ax5.set_xlabel('List Size')
    ax5.set_ylabel('Time to delete (μs)')
    ax5.grid(True)

    # Find - should be O(n)
    sizes, times = benchmark_find()
    ax6.plot(sizes, times, 'orange', marker='o')
    ax6.set_title('Find Last Element (Should be O(n))')
    ax6.set_xlabel('List Size')
    ax6.set_ylabel('Time to find (μs)')
    ax6.grid(True)

    plt.tight_layout()
    plt.savefig('singly_linked_list_benchmarks.png', dpi=150, bbox_inches='tight')
    print("\nBenchmark plot saved as 'singly_linked_list_benchmarks.png'")


if __name__ == "__main__":
    plot_results()