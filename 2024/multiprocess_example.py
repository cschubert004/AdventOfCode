import multiprocessing
import queue
import itertools
import time


# a utility function to get us a slice of an iterator, as an iterator
# when working with iterators maximum lazyness is preferred
def iterator_slice(iterator, length):
    iterator = iter(iterator)
    while True:
        res = tuple(itertools.islice(iterator, length))
        if not res:
            break
        yield res


def is_power_of_two(n):
    return (n & (n - 1) == 0) and n != 0


def worker(input_queue, output_queue):
    while True:
        # time.sleep(0.2)  # Simulate work
        try:
            value = input_queue.get(timeout=1)
            if value is not None and value % 1000 == 0:
                print(f"Testing value {value}")
            # Exit if None in queue
            if value is None:
                break
            if is_power_of_two(value):
                output_queue.put(value)
        except queue.Empty:
            time.sleep(0.001)


def main():
    input_values = range(1, 6000)  # Example iterator
    # Iterator slicer - put items in the queue X at a time
    count_iterator = iterator_slice(input_values, 10000)
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    tq = []

    for values in next(count_iterator):
        input_queue.put(values)
        tq.append(values)

    num_processes = 4
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    # Feed the queue
    while count_iterator:
        if input_queue.empty() or input_queue.qsize() < 1000:
            try:
                values = next(count_iterator)
                # print(f"Adding {len(values)} values to the queue")
                for value in values:
                    input_queue.put(value)
                time.sleep(0.01)  # Wait for the queue thread to catch up
            except StopIteration:
                break
        else:
            time.sleep(0.01)

    # stop the queue
    print("Stopping Queues")
    for _ in range(num_processes + 1):
        input_queue.put(None)

    for p in processes:
        p.join()

    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    print("Powers of 2:", results)


if __name__ == "__main__":
    main()
