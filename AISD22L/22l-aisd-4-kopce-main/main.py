from heap import NHeap
import gc
import random
import time
import matplotlib.pyplot as plt


def measure_pop_heap(heap, repeat):
    gc_old = gc.isenabled()  # pobierz aktualny stan odśmiecania gc.disable()
    gc.disable()
    # measure the loop
    start = time.time()
    for i in range(repeat):
        heap.pop()

    delta = time.time() - start

    if gc_old:
        gc.enable()
    return delta


def measure_function(fun, args, iter=1):
    """
    helper function to measure execution, disables gc
    :param fun: function reference
    :param args: tuple of args
    :param iter: amount of iterations
    :return: average time taken (in milliseconds), max deviation
    """

    gc_old = gc.isenabled()  # pobierz aktualny stan odśmiecania gc.disable()
    gc.disable()
    # measure
    results = []
    for i in range(iter):
        start = time.time()
        fun(*args)
        delta = time.time() - start
        results.append(delta)

    if gc_old:
        gc.enable()
    avg = sum(results) / len(results)
    biggest_deviation = max(abs(avg - max(results)), abs(avg - min(results)))
    return avg


# matplotlib
def draw_functions_on_one_plot(data, fname="all"):
    # draw all functions on one plot
    for name, times in data.items():
        x = [time[0] for time in times]
        y = [time[1] for time in times]
        plt.plot(x, y, label=name)
        plt.xlabel("Heap size")
        plt.ylabel("Time(s)")
    plt.legend()
    plt.title("All algorithms")
    plt.savefig(fname + ".jpg", format="jpg", dpi=200)


def draw_separately(data):
    # draw each function on separate plot
    for name, times in data.items():
        plt.figure()
        x = [time[0] for time in times]
        y = [time[1] for time in times]
        plt.plot(x, y)
        plt.xlabel("Heap size")
        plt.ylabel("Time(s)")
        plt.title(name)
        plt.savefig(name + ".jpg", format="jpg", dpi=200)


def main():
    cases_create = range(10000, 1000000, 10000)
    cases_delete = range(10000, 300000, 10000)

    # 300000x random numbers from 0 to 100000
    data = random.sample(range(1000000), 1000000)

    results_create = {
        "2-create": [],
        "3-create": [],
        "4-create": [],
    }
    results_delete = {
        "2-delete": [],
        "3-delete": [],
        "4-delete": [],
    }

    # create
    for n in (2, 3, 4):
        key = f'{n}-create'
        for case in cases_create:
            print("create n:", n, "case:", case)
            results_create[key].append((case, measure_function(NHeap, (n, data[:case]))))

    # delete
    for n in (2, 3, 4):
        deleter = NHeap(n, data)  # create heap from full data first
        backup_arr = deleter._array[:]  # copy
        key = f'{n}-delete'
        for case in cases_delete:
            print("delete n:", n, "case:", case)
            results_delete[key].append((case, measure_pop_heap(deleter, case)))
            deleter._array = backup_arr[:]

    draw_separately(results_create)
    draw_functions_on_one_plot(results_create, "all_create")
    draw_separately(results_delete)
    draw_functions_on_one_plot(results_delete, "all_delete")


def test():
    h = NHeap(4, random.sample(range(100), 100))
    h.printHeap()


if __name__ == "__main__":
    test()
