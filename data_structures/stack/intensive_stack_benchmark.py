import time
import matplotlib.pyplot as plt
import psutil
import os
from stack_array import StackArray
from stack import Stack


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def benchmark_large_sizes():
    """Test with very large stack sizes to find crossover point"""
    print("=== Large Size Benchmark ===")
    sizes = [100000, 500000, 1000000, 2000000]

    array_push_times = []
    linked_push_times = []

    for size in sizes:
        print(f"\nTesting size: {size:,}")

        # Array benchmark
        s_array = StackArray()
        start = time.perf_counter()
        for i in range(size):
            s_array.push(i)
        array_time = time.perf_counter() - start
        avg_array = (array_time / size) * 1000000
        array_push_times.append(avg_array)
        print(f"  Array: {avg_array:.3f} μs per push")

        # Linked list benchmark
        s_linked = Stack()
        start = time.perf_counter()
        for i in range(size):
            s_linked.push(i)
        linked_time = time.perf_counter() - start
        avg_linked = (linked_time / size) * 1000000
        linked_push_times.append(avg_linked)
        print(f"  Linked: {avg_linked:.3f} μs per push")

        print(f"  Ratio (Linked/Array): {avg_linked/avg_array:.2f}x")

        del s_array, s_linked  # Free memory

    return sizes, array_push_times, linked_push_times


def benchmark_memory_usage():
    """Compare memory usage patterns"""
    print("\n=== Memory Usage Benchmark ===")
    size = 500000

    print(f"Baseline memory: {get_memory_usage():.1f} MB")

    # Array memory usage
    start_mem = get_memory_usage()
    s_array = StackArray()
    for i in range(size):
        s_array.push(i)
    array_mem = get_memory_usage() - start_mem
    print(f"Array memory usage: {array_mem:.1f} MB")
    del s_array

    # Wait for garbage collection
    import gc
    gc.collect()
    time.sleep(0.1)

    # Linked list memory usage
    start_mem = get_memory_usage()
    s_linked = Stack()
    for i in range(size):
        s_linked.push(i)
    linked_mem = get_memory_usage() - start_mem
    print(f"Linked list memory usage: {linked_mem:.1f} MB")
    print(f"Memory efficiency (Array/Linked): {array_mem/linked_mem:.2f}x")
    del s_linked


def benchmark_resize_stress():
    """Test worst-case scenarios that trigger array resizes"""
    print("\n=== Resize Stress Test ===")

    # Test push patterns that will trigger multiple resizes
    resize_triggers = [2**i for i in range(10, 21)]  # Powers of 2 from 1K to 1M

    array_worst_times = []
    linked_times = []

    for size in resize_triggers:
        print(f"\nTesting resize stress at {size:,} elements")

        # Array - measure time for operations that trigger resize
        s_array = StackArray()
        # Pre-fill to just before resize trigger
        for i in range(size - 100):
            s_array.push(i)

        # Measure the last 100 pushes (some will trigger resize)
        start = time.perf_counter()
        for i in range(100):
            s_array.push(size + i)
        array_time = (time.perf_counter() - start) / 100 * 1000000
        array_worst_times.append(array_time)
        print(f"  Array (near resize): {array_time:.3f} μs per push")

        # Linked list - same pattern
        s_linked = Stack()
        for i in range(size - 100):
            s_linked.push(i)

        start = time.perf_counter()
        for i in range(100):
            s_linked.push(size + i)
        linked_time = (time.perf_counter() - start) / 100 * 1000000
        linked_times.append(linked_time)
        print(f"  Linked: {linked_time:.3f} μs per push")

        del s_array, s_linked

    return resize_triggers, array_worst_times, linked_times


def benchmark_burst_patterns():
    """Test rapid push/pop cycles"""
    print("\n=== Burst Pattern Benchmark ===")

    burst_sizes = [1000, 5000, 10000, 50000, 100000]
    array_burst_times = []
    linked_burst_times = []

    for burst_size in burst_sizes:
        print(f"\nTesting burst pattern: {burst_size:,} push/pop cycles")

        # Array burst test
        s_array = StackArray()
        start = time.perf_counter()
        for cycle in range(10):  # 10 burst cycles
            for i in range(burst_size):
                s_array.push(i)
            for i in range(burst_size):
                s_array.pop()
        array_time = (time.perf_counter() - start) / (10 * 2 * burst_size) * 1000000
        array_burst_times.append(array_time)
        print(f"  Array: {array_time:.3f} μs per operation")

        # Linked list burst test
        s_linked = Stack()
        start = time.perf_counter()
        for cycle in range(10):  # 10 burst cycles
            for i in range(burst_size):
                s_linked.push(i)
            for i in range(burst_size):
                s_linked.pop()
        linked_time = (time.perf_counter() - start) / (10 * 2 * burst_size) * 1000000
        linked_burst_times.append(linked_time)
        print(f"  Linked: {linked_time:.3f} μs per operation")

        del s_array, s_linked

    return burst_sizes, array_burst_times, linked_burst_times


def benchmark_size_operation():
    """Compare size() operation performance"""
    print("\n=== Size Operation Benchmark ===")

    sizes = [10000, 50000, 100000, 500000]
    array_size_times = []
    linked_size_times = []

    for size in sizes:
        print(f"\nTesting size() with {size:,} elements")

        # Pre-populate both stacks
        s_array = StackArray()
        s_linked = Stack()
        for i in range(size):
            s_array.push(i)
            s_linked.push(i)

        # Test array size() - should be O(1)
        start = time.perf_counter()
        for _ in range(1000):
            s_array.size()
        array_time = (time.perf_counter() - start) / 1000 * 1000000
        array_size_times.append(array_time)
        print(f"  Array size(): {array_time:.3f} μs")

        # Test linked size() - O(n)
        start = time.perf_counter()
        s_linked.size()  # Only once since it's expensive
        linked_time = (time.perf_counter() - start) * 1000000
        linked_size_times.append(linked_time)
        print(f"  Linked size(): {linked_time:.3f} μs")

        del s_array, s_linked

    return sizes, array_size_times, linked_size_times


def plot_intensive_results():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, _)) = plt.subplots(3, 2, figsize=(16, 12))

    # Large size comparison
    sizes, array_times, linked_times = benchmark_large_sizes()
    ax1.plot(sizes, array_times, 'b-o', label='Array-based', linewidth=2, markersize=6)
    ax1.plot(sizes, linked_times, 'r-s', label='Linked List', linewidth=2, markersize=6)
    ax1.set_title('Large Size Push Performance')
    ax1.set_xlabel('Stack Size')
    ax1.set_ylabel('Time per push (μs)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')

    # Memory usage
    benchmark_memory_usage()

    # Resize stress
    sizes, array_worst, linked_times = benchmark_resize_stress()
    ax2.plot(sizes, array_worst, 'b-o', label='Array (resize stress)', linewidth=2, markersize=6)
    ax2.plot(sizes, linked_times, 'r-s', label='Linked List', linewidth=2, markersize=6)
    ax2.set_title('Resize Stress Test')
    ax2.set_xlabel('Stack Size (resize triggers)')
    ax2.set_ylabel('Time per push (μs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')

    # Burst patterns
    sizes, array_burst, linked_burst = benchmark_burst_patterns()
    ax3.plot(sizes, array_burst, 'b-o', label='Array-based', linewidth=2, markersize=6)
    ax3.plot(sizes, linked_burst, 'r-s', label='Linked List', linewidth=2, markersize=6)
    ax3.set_title('Burst Pattern Performance')
    ax3.set_xlabel('Burst Size')
    ax3.set_ylabel('Time per operation (μs)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Size operation
    sizes, array_size, linked_size = benchmark_size_operation()
    ax4.plot(sizes, array_size, 'b-o', label='Array size() - O(1)', linewidth=2, markersize=6)
    ax4.plot(sizes, linked_size, 'r-s', label='Linked size() - O(n)', linewidth=2, markersize=6)
    ax4.set_title('Size Operation Performance')
    ax4.set_xlabel('Stack Size')
    ax4.set_ylabel('Time (μs)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_yscale('log')

    # Performance ratio over size
    ratio_sizes, ratio_array, ratio_linked = benchmark_large_sizes()
    ratios = [l/a for a, l in zip(ratio_array, ratio_linked)]
    ax5.plot(ratio_sizes, ratios, 'g-o', linewidth=2, markersize=6)
    ax5.axhline(y=1.0, color='black', linestyle='--', alpha=0.7, label='Equal performance')
    ax5.set_title('Performance Ratio (Linked/Array)')
    ax5.set_xlabel('Stack Size')
    ax5.set_ylabel('Ratio (>1 = Linked slower)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_xscale('log')

    plt.tight_layout()
    plt.savefig('intensive_stack_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\n\nIntensive comparison plot saved as 'intensive_stack_comparison.png'")


if __name__ == "__main__":
    plot_intensive_results()