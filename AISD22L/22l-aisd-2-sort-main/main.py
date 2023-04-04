import sys
import time
import gc
from plotter import plotter
from sorting_algs import bubble_sort, merge_sort, quick_sort_run, selection_sort


# optionally limits the amount of words
def load_words_from_file(path, n=-1):
    with open(path, "r", encoding="UTF-8") as f:
        words = []
        # dzieli linie na słowa po spacjach
        # ignoruje każde słowo zawierające cokolwiek innego niż litery
        for line in [line.rstrip().split(" ") for line in f.readlines()]:
            words.extend(line)
        words = [word.lower() for word in words if word.isalpha()]
        return words[:n] if n > 0 else words


def measure_function(fun, in_array, iter=1):
    """
    helper function to measure sort, disables gc
    :param fun: sorting function reference
    :param in_array: array to sort
    :param iter: amount of iterations
    :return: average time taken (in milliseconds), max deviation
    """

    # make a copy of what we are sorting for iterations
    in_array_copy = in_array.copy()
    gc_old = gc.isenabled()  # pobierz aktualny stan odśmiecania gc.disable()
    gc.disable()
    # measure
    results = []
    for i in range(iter):
        start = time.time()
        fun(in_array_copy)
        delta = time.time()-start
        results.append(delta)
        in_array_copy = in_array.copy()

    if gc_old:
        gc.enable()
    avg = sum(results)/len(results)
    biggest_deviation = max(abs(avg-max(results)), abs(avg-min(results)))
    return avg, biggest_deviation


def get_data(array, testcases):
    """
    runs testcases and returns dict with times for each function
    """
    results = {}
    for testcase in testcases:
        print(f"\ntesting {testcase} words\n")
        for function in (quick_sort_run, merge_sort, bubble_sort, selection_sort, sorted):
            if function in [bubble_sort, selection_sort] and testcase > 2000:
                continue
            time, deviation = measure_function(function, array[:testcase], 5)

            if function.__name__ not in results:
                results[function.__name__] = [(testcase, time)]
            else:
                results[function.__name__].append((testcase, time))

    return results


def main():
    sys.setrecursionlimit(100000)
    array = load_words_from_file("pan-tadeusz.txt")
    data = get_data(array, list(range(100, 25000, 100)))
    plotter(data)


if __name__ == "__main__":
    main()
