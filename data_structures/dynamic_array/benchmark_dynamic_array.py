import time
import matplotlib.pyplot as plt
from dynamic_array import DynamicArray


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def benchmark_append():
    print("Benchmarking append...")
    sizes = [1000, 2000, 4000, 8000, 16000, 32000]
    times = []

    for size in sizes:
        arr = DynamicArray()
        total_time = 0

        for i in range(size):
            elapsed, _ = time_operation(arr.append, i)
            total_time += elapsed

        avg_time = total_time / size
        times.append(avg_time * 1000000)  # Convert to microseconds
        print(f"Size {size}: {avg_time * 1000000:.2f} μs per append")

    return sizes, times


def benchmark_get():
    print("\nBenchmarking get...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    times = []

    for size in sizes:
        arr = DynamicArray()
        for i in range(size):
            arr.append(i)

        # Test random access
        import random
        indices = [random.randint(0, size-1) for _ in range(1000)]

        start = time.perf_counter()
        for idx in indices:
            arr.get(idx)
        end = time.perf_counter()

        avg_time = (end - start) / 1000
        times.append(avg_time * 1000000)
        print(f"Size {size}: {avg_time * 1000000:.2f} μs per get")

    return sizes, times


def benchmark_insert():
    print("\nBenchmarking insert at beginning...")
    sizes = [1000, 2000, 3000, 4000, 5000]
    times = []

    for size in sizes:
        arr = DynamicArray()
        for i in range(size):
            arr.append(i)

        # Insert at beginning (worst case)
        elapsed, _ = time_operation(arr.insert, 0, 999)
        times.append(elapsed * 1000000)
        print(f"Size {size}: {elapsed * 1000000:.2f} μs to insert at beginning")

    return sizes, times


def benchmark_delete():
    print("\nBenchmarking delete from beginning...")
    sizes = [1000, 2000, 3000, 4000, 5000]
    times = []

    for size in sizes:
        arr = DynamicArray()
        for i in range(size):
            arr.append(i)

        # Delete from beginning (worst case)
        elapsed, _ = time_operation(arr.delete, 0)
        times.append(elapsed * 1000000)
        print(f"Size {size}: {elapsed * 1000000:.2f} μs to delete from beginning")

    return sizes, times


def plot_results():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # Append
    sizes, times = benchmark_append()
    ax1.plot(sizes, times, 'b-o')
    ax1.set_title('Append Performance (Should be O(1) amortized)')
    ax1.set_xlabel('Array Size')
    ax1.set_ylabel('Time per append (μs)')
    ax1.grid(True)

    # Get
    sizes, times = benchmark_get()
    ax2.plot(sizes, times, 'g-o')
    ax2.set_title('Get Performance (Should be O(1))')
    ax2.set_xlabel('Array Size')
    ax2.set_ylabel('Time per get (μs)')
    ax2.grid(True)

    # Insert
    sizes, times = benchmark_insert()
    ax3.plot(sizes, times, 'r-o')
    ax3.set_title('Insert at Beginning (Should be O(n))')
    ax3.set_xlabel('Array Size')
    ax3.set_ylabel('Time to insert (μs)')
    ax3.grid(True)

    # Delete
    sizes, times = benchmark_delete()
    ax4.plot(sizes, times, 'm-o')
    ax4.set_title('Delete from Beginning (Should be O(n))')
    ax4.set_xlabel('Array Size')
    ax4.set_ylabel('Time to delete (μs)')
    ax4.grid(True)

    plt.tight_layout()
    plt.savefig('dynamic_array_benchmarks.png', dpi=150, bbox_inches='tight')
    print("\nBenchmark plot saved as 'dynamic_array_benchmarks.png'")


if __name__ == "__main__":
    # Remove debug print from get method first
    plot_results()