# import sys
from cmath import inf
import time
import gc
from plotter import plotter
import algorythms


def get_text_from_file(path):
    info = ""
    with open(path, "r", encoding="UTF-8") as f:
        for line in f:
            info += line.rstrip()
            info += " " if len(line) != 1 else ""
    return info


#  optionally limits the amount of words
def load_words_from_file(path, n=-1):
    # with open(path, "r", encoding="UTF-8") as f:
    # words = []
    # dzieli linie na słowa po spacjach
    # ignoruje każde słowo zawierające cokolwiek innego niż litery
    # for line in [line.rstrip().split(" ") for line in f.readlines()]:
    #    words.extend(line)
    # words = [word for word in words if word.isalpha()]
    text = get_text_from_file(path)
    return text[:n] if n > 0 else text


def measure_function(fun, pattern, text, iter=1):
    """
    helper function to measure sort, disables gc
    :param fun: function reference
    :param iter: amount of iterations
    :return: average time taken (in milliseconds), max deviation
    """

    gc_old = gc.isenabled()  # pobierz aktualny stan odśmiecania gc.disable()
    gc.disable()
    # measure
    results = []
    for i in range(iter):
        start = time.time()
        fun(pattern, text)
        delta = time.time() - start
        results.append(delta)

    if gc_old:
        gc.enable()
    avg = sum(results) / len(results)
    biggest_deviation = max(abs(avg - max(results)), abs(avg - min(results)))
    return avg, biggest_deviation


def get_data(plaintext, words_to_find: str, ranges):
    """
    runs testcases and returns dict with times for each function
    """
    results = {"naive": [], "KMP": [], "rabin-karp": []}
    for case in ranges:
        print("testing:", case)
        s1, s2, s3 = 0, 0, 0
        # transforming words_to_find into list of needed words for this case
        word = words_to_find.split(" ")[:case]
        word = " ".join(word)  # transforming it back into string
        # word = words_to_find[:case]
        s1 += measure_function(algorythms.naive, word, plaintext)[0]
        s2 += measure_function(algorythms.KMP, word, plaintext)[0]
        s3 += measure_function(algorythms.rabin_karp, word, plaintext)[0]
        results["naive"].append((case, s1))
        results["KMP"].append((case, s2))
        results["rabin-karp"].append((case, s3))
    return results


def main():
    # sys.setrecursionlimit(100000)
    words = load_words_from_file("pan-tadeusz.txt")
    whole_file = get_text_from_file("pan-tadeusz.txt")
    data = get_data(whole_file, words, list(range(1, 60001, 500)))
    plotter(data)


if __name__ == "__main__":
    main()
