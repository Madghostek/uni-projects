def naive(pattern, text):
    s, m = len(pattern), len(text)
    indexes = []
    if s == 0 or m == 0:
        return indexes
    for i in range(0, m - s + 1):
        cut = text[i : i + s]
        if pattern == cut:
            indexes.append(i)
    return indexes


def rabin_karp(pattern, text, prime_number=65449, digit=380):
    indexes = []
    s = len(pattern)
    m = len(text)
    if s == 0 or m == 0:
        return indexes
    # the value that the number "1" acquires,
    # placed to the high order of the s-digit number
    h = (digit ** (s - 1)) % prime_number
    pattern_as_number = 0
    text_as_number = 0
    for i in range(s):
        # calculating the value of pattern treating each letter as a number
        pattern_as_number = (digit * pattern_as_number + ord(pattern[i])) % prime_number
        text_as_number = (digit * text_as_number + ord(text[i])) % prime_number
    # pattern_as_number %= prime_number
    # text_as_number %= prime_number
    for i in range(m - s + 1):
        cut = text[i : i + s]
        if pattern_as_number == text_as_number:
            # unequal numbers can have the same result of mod operation,
            # so we need to check if text cut is actualy equal to pattern
            if pattern == cut:
                indexes.append(i)
        if i < m - s:
            # calculating the next value of text_as_number cut shifted one position right,
            # based on the previous value of text_as_number
            text_as_number = (
                digit * (text_as_number - ord(text[i]) * h) + ord(text[i + s])
            ) % prime_number
    return indexes


# for KMP
# returns table that describes maximum suffix=prefix part of the pattern
# ith index - substring of pattern spanning from 0 to i+1
# so e.g. i=0 -> substring of length 1
# tab[0]=0 because can't take whole word as a prefix/suffix
def make_prefix_table(pattern):
    tab = [0] * (len(pattern))  # prepare output table
    current = 0  # second pointer to compare
    for i in range(1, len(pattern)):  # start from 1 - tab[0]=0 always
        while pattern[i] != pattern[current] and current:
            current = tab[current - 1]

        # if current char and pointer are equal, increase current and remember
        if pattern[i] == pattern[current]:
            current += 1
            tab[i] = current

    return tab


def KMP(pattern, text):
    p_table = make_prefix_table(pattern)
    result = []
    t, p = 0, 0  # text and pattern pointer
    # t is incremented every loop iteration,
    # unless pattern pointer was moved back (must check current spot again)
    if len(pattern) == 0 or len(text) == 0:
        return result  # edge cases
    while t < len(text):
        if text[t] == pattern[p]:
            p += 1
            if p == len(pattern):  # end of pattern and a match
                result.append(t - p + 1)  # text pointer, but p chars back = start
                # move back the pointer at this moment as well,
                # don't just restart
                if p != 0:
                    p = p_table[p - 1]
            t += 1  # increment
        else:
            # on error, move 'p' back, but use information about the pattern
            # to find optimal place
            if p != 0:
                p = p_table[p - 1]
            else:
                t += 1  # increment

    return result


def main():
    pattern = ""
    text = "ABAABAAABAAAABAAAAA"
    print(KMP(pattern, text))


if __name__ == "__main__":
    main()
