def bubble_sort(tab):
    for i in range(len(tab)):
        for j in range(len(tab) - i - 1):
            if tab[j] > tab[j + 1]:
                # changing two neighboring elements
                var = tab[j]
                tab[j] = tab[j + 1]
                tab[j + 1] = var
    return tab


def quick_sort_run(tab):
    return quick_sort(tab, 0, len(tab)-1)


def quick_sort(tab, low, high):
    """
    1. Sort the whole list by some element(pivot): all smaller elements are on the left, bigger - on the right
    2. Divide list in two parts by pivot
    3. Use the same algorythm for the parts
    4. Stop when parts are 1 element long
    """
    def partition(tab, low, high):
        """
        1. Pick an element from the list(pivot)
        2. Pick a bigger element than pivot from the left
        3. Pick a smaller element than pivot from the right
        4. Swap these elements
        5. Stop when elements meet and change sides
        """
        pivot = tab[low]
        i = low
        j = high
        while i < j:
            while not tab[i] > pivot and i < high:
                i += 1
            # found an element bigger than pivot on the left
            while not tab[j] < pivot and j > low:
                j -= 1
            # found an element smaller than pivot on the right
            if i < j:
                # swap elements
                var = tab[i]
                tab[i] = tab[j]
                tab[j] = var
        # put pivot in the place of smaller element in j index
        var = tab[j]
        tab[j] = pivot
        tab[low] = var
        # return new index of pivot
        return j

    if low < high:
        j = partition(tab, low, high)
        quick_sort(tab, low, j)
        quick_sort(tab, j + 1, high)
    return tab


def selection_sort(tab):
    """
    Selects smallest element and swaps it with element at the pointer `ptr`.
    """

    for ptr in range(len(tab)):
        min_el = tab[ptr]
        min_idx = ptr
        for i in range(ptr, len(tab)):
            if tab[i] < min_el:
                min_el = tab[i]
                min_idx = i
        # zamień ptr ze znalezionym kandydatem
        tab[ptr], tab[min_idx] = tab[min_idx], tab[ptr]
    return tab


def merge_sort(tab):
    """
    1. Divide array into 2 parts
    2. Sort the parts (recursive call)
    3. merge

    It's impossible to do this "in place", it is required to keep the halves
    in a helper lists or one big list. Here lists are created on the go.
    """

    # Merge two (sorted!!) lists into bigger sorted list, uses existing `dest` list
    def merge(dest, A, B):
        left, right, ptr = 0, 0, 0
        while ptr < len(dest):
            if right >= len(B) or (left < len(A) and A[left] < B[right]):
                dest[ptr] = A[left]
                left += 1
            else:
                dest[ptr] = B[right]
                right += 1
            ptr += 1

    if len(tab) < 2:
        return tab
    mid = len(tab) // 2
    A, B = tab[:mid], tab[mid:]
    A, B = merge_sort(A), merge_sort(B)
    # the existing list is used to reduce reallocations
    merge(tab, A, B)
    return tab