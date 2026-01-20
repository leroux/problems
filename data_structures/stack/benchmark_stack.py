import time
import matplotlib.pyplot as plt
from stack import Stack


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def benchmark_push():
    print("Benchmarking push...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    times = []

    for size in sizes:
        s = Stack()
        total_time = 0

        for i in range(size):
            elapsed, _ = time_operation(s.push, i)
            total_time += elapsed

        avg_time = total_time / size
        times.append(avg_time * 1000000)  # Convert to microseconds
        print(f"Size {size}: {avg_time * 1000000:.2f} μs per push")

    return sizes, times


def benchmark_pop():
    print("\nBenchmarking pop...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    times = []

    for size in sizes:
        # Pre-populate stack
        s = Stack()
        for i in range(size):
            s.push(i)

        total_time = 0
        for i in range(size):
            elapsed, _ = time_operation(s.pop)
            total_time += elapsed

        avg_time = total_time / size
        times.append(avg_time * 1000000)
        print(f"Size {size}: {avg_time * 1000000:.2f} μs per pop")

    return sizes, times


def benchmark_peek():
    print("\nBenchmarking peek...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    times = []

    for size in sizes:
        # Pre-populate stack
        s = Stack()
        for i in range(size):
            s.push(i)

        # Perform many peeks
        total_time = 0
        num_peeks = 1000
        for i in range(num_peeks):
            elapsed, _ = time_operation(s.peek)
            total_time += elapsed

        avg_time = total_time / num_peeks
        times.append(avg_time * 1000000)
        print(f"Stack size {size}: {avg_time * 1000000:.2f} μs per peek")

    return sizes, times


def benchmark_size():
    print("\nBenchmarking size...")
    sizes = [10000, 20000, 40000, 80000, 160000]
    times = []

    for size in sizes:
        # Pre-populate stack
        s = Stack()
        for i in range(size):
            s.push(i)

        # Measure size() operation
        elapsed, _ = time_operation(s.size)
        times.append(elapsed * 1000000)
        print(f"Stack size {size}: {elapsed * 1000000:.2f} μs to get size")

    return sizes, times


def benchmark_mixed_operations():
    print("\nBenchmarking mixed operations (push/pop pattern)...")
    sizes = [1000, 2000, 4000, 8000, 16000]
    times = []

    for size in sizes:
        s = Stack()

        start = time.perf_counter()
        # Pattern: push N, pop N/2, push N/2, pop all
        for i in range(size):
            s.push(i)

        for i in range(size // 2):
            s.pop()

        for i in range(size // 2):
            s.push(i + size)

        while not s.is_empty():
            s.pop()
        end = time.perf_counter()

        total_time = end - start
        times.append(total_time * 1000000)
        print(f"Size {size}: {total_time * 1000000:.2f} μs for mixed operations")

    return sizes, times


def plot_results():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, _)) = plt.subplots(3, 2, figsize=(14, 12))

    # Push - should be O(1)
    sizes, times = benchmark_push()
    ax1.plot(sizes, times, 'b-o')
    ax1.set_title('Push Performance (Should be O(1))')
    ax1.set_xlabel('Stack Size')
    ax1.set_ylabel('Time per push (μs)')
    ax1.grid(True)

    # Pop - should be O(1)
    sizes, times = benchmark_pop()
    ax2.plot(sizes, times, 'r-o')
    ax2.set_title('Pop Performance (Should be O(1))')
    ax2.set_xlabel('Stack Size')
    ax2.set_ylabel('Time per pop (μs)')
    ax2.grid(True)

    # Peek - should be O(1)
    sizes, times = benchmark_peek()
    ax3.plot(sizes, times, 'g-o')
    ax3.set_title('Peek Performance (Should be O(1))')
    ax3.set_xlabel('Stack Size')
    ax3.set_ylabel('Time per peek (μs)')
    ax3.grid(True)

    # Size - depends on implementation (O(1) or O(n))
    sizes, times = benchmark_size()
    ax4.plot(sizes, times, 'm-o')
    ax4.set_title('Size Performance (O(1) if cached, O(n) if counted)')
    ax4.set_xlabel('Stack Size')
    ax4.set_ylabel('Time to get size (μs)')
    ax4.grid(True)

    # Mixed operations
    sizes, times = benchmark_mixed_operations()
    ax5.plot(sizes, times, 'c-o')
    ax5.set_title('Mixed Operations (Push/Pop Pattern)')
    ax5.set_xlabel('Operation Size')
    ax5.set_ylabel('Total time (μs)')
    ax5.grid(True)

    plt.tight_layout()
    plt.savefig('stack_benchmarks.png', dpi=150, bbox_inches='tight')
    print("\nBenchmark plot saved as 'stack_benchmarks.png'")


if __name__ == "__main__":
    plot_results()