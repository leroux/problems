import time
import matplotlib.pyplot as plt
from stack_array import StackArray


def time_operation(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start, result


def benchmark_implementation(StackClass, name):
    print(f"\n=== Benchmarking {name} ===")

    def benchmark_push():
        print("Benchmarking push...")
        sizes = [10000, 20000, 40000, 80000, 160000]
        times = []

        for size in sizes:
            s = StackClass()
            total_time = 0

            for i in range(size):
                elapsed, _ = time_operation(s.push, i)
                total_time += elapsed

            avg_time = total_time / size
            times.append(avg_time * 1000000)
            print(f"  Size {size}: {avg_time * 1000000:.2f} μs per push")

        return sizes, times

    def benchmark_pop():
        print("Benchmarking pop...")
        sizes = [10000, 20000, 40000, 80000, 160000]
        times = []

        for size in sizes:
            s = StackClass()
            for i in range(size):
                s.push(i)

            total_time = 0
            for i in range(size):
                elapsed, _ = time_operation(s.pop)
                total_time += elapsed

            avg_time = total_time / size
            times.append(avg_time * 1000000)
            print(f"  Size {size}: {avg_time * 1000000:.2f} μs per pop")

        return sizes, times

    def benchmark_peek():
        print("Benchmarking peek...")
        sizes = [10000, 20000, 40000, 80000, 160000]
        times = []

        for size in sizes:
            s = StackClass()
            for i in range(size):
                s.push(i)

            total_time = 0
            num_peeks = 1000
            for i in range(num_peeks):
                elapsed, _ = time_operation(s.peek)
                total_time += elapsed

            avg_time = total_time / num_peeks
            times.append(avg_time * 1000000)
            print(f"  Stack size {size}: {avg_time * 1000000:.2f} μs per peek")

        return sizes, times

    return {
        'push': benchmark_push(),
        'pop': benchmark_pop(),
        'peek': benchmark_peek()
    }


def plot_comparison():
    # Benchmark array-based stack
    array_results = benchmark_implementation(StackArray, "Array-based Stack")

    # Import and benchmark linked list stack after user implements it
    try:
        from stack import Stack
        linked_results = benchmark_implementation(Stack, "Linked List Stack")
    except ImportError:
        print("\nLinked list stack not implemented yet. Showing only array results.")
        linked_results = None

    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Push comparison
    sizes, array_push_times = array_results['push']
    ax1.plot(sizes, array_push_times, 'b-o', label='Array-based', linewidth=2)
    if linked_results:
        _, linked_push_times = linked_results['push']
        ax1.plot(sizes, linked_push_times, 'r-s', label='Linked List', linewidth=2)
    ax1.set_title('Push Performance Comparison')
    ax1.set_xlabel('Stack Size')
    ax1.set_ylabel('Time per push (μs)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Pop comparison
    sizes, array_pop_times = array_results['pop']
    ax2.plot(sizes, array_pop_times, 'b-o', label='Array-based', linewidth=2)
    if linked_results:
        _, linked_pop_times = linked_results['pop']
        ax2.plot(sizes, linked_pop_times, 'r-s', label='Linked List', linewidth=2)
    ax2.set_title('Pop Performance Comparison')
    ax2.set_xlabel('Stack Size')
    ax2.set_ylabel('Time per pop (μs)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Peek comparison
    sizes, array_peek_times = array_results['peek']
    ax3.plot(sizes, array_peek_times, 'b-o', label='Array-based', linewidth=2)
    if linked_results:
        _, linked_peek_times = linked_results['peek']
        ax3.plot(sizes, linked_peek_times, 'r-s', label='Linked List', linewidth=2)
    ax3.set_title('Peek Performance Comparison')
    ax3.set_xlabel('Stack Size')
    ax3.set_ylabel('Time per peek (μs)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('stack_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\nComparison plot saved as 'stack_comparison.png'")


if __name__ == "__main__":
    plot_comparison()