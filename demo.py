"""
(cre) demonstration and performance comparison script.
This is a simple script to show performance comparisonusing with very
basic patterns. Stats with real regular expressions can be different.
"""
import re
import time
import string
import random
from threading import Thread

import cre

DIGITS = string.digits
LETTERS = string.ascii_lowercase

STRING_COUNT = 10000
STRING_LENGTH = 70
PATTERN_COUNT = 1000
PATTERN_LENGTH = 5
CRE_THREAD_COUNT = 4


def generate_rand_str(str_length):
    """
    Generate random string of alphabets and digits.
    """
    return ''.join(random.choice(LETTERS+DIGITS)
                   for _ in range(str_length))


def search(patterns, strings, matches):
    """
    Search patterns is strings.
    """
    for string in strings:
        for pattern in patterns:
            if pattern.search(string):
                matches.append(string)
                break


def search_with_re(patterns, strings):
    """
    Do search using (re) module.
    """
    start = time.time()
    # Compile patterns:
    c_patterns = [re.compile(pattern) for pattern in patterns]

    matches = []
    search(c_patterns, strings, matches)
    elapsed_time = time.time() - start

    return elapsed_time, matches


def search_with_cre(patterns, strings, thread_cou):
    """
    Do search using (cre) module.
    """
    start = time.time()
    # Compile patterns:
    c_patterns = [cre.compile(pattern) for pattern in patterns]

    matches = []
    # Split search across threads:
    step = int(len(strings) / thread_cou)
    s_idx = 0
    e_idx = step
    threads = []
    for _ in range(thread_cou):
        thr = Thread(target=search, args=(c_patterns, strings[s_idx:e_idx], \
                                          matches))
        thr.daemon = True
        threads.append(thr)
        thr.start()
        s_idx = e_idx
        e_idx = (e_idx+step) if (e_idx+step) < len(strings) else len(strings)
    for thr in threads:
        thr.join()

    elapsed_time = time.time() - start

    return elapsed_time, matches


def demo():
    """
    Run demonstration.
    """
    print('Generating random strings')
    strings = [generate_rand_str(STRING_LENGTH) \
               for _ in range(STRING_COUNT)]
    print('Strings count: {0}'.format(len(strings)))
    print('Generating random patterns')
    patterns = ['.*' + generate_rand_str(PATTERN_LENGTH) + '.*' \
                for _ in range(PATTERN_COUNT)]
    print('Patterns count: {0}'.format(len(patterns)))

    print('Searching strings for generated patterns using (re)')
    elapsed_time, matches_re = search_with_re(patterns, strings)
    print('Matches: {0}'.format(len(matches_re)))
    print('Elapsed Time: {0}'.format(elapsed_time))

    time.sleep(3)

    print('Searching strings for generated patterns using (cre)')
    print('Number of threads: {0}'.format(CRE_THREAD_COUNT))
    elapsed_time, matches_cre = search_with_cre(patterns, strings, \
                                                CRE_THREAD_COUNT)
    print('Matches: {0}'.format(len(matches_cre)))
    print('Elapsed Time: {0}'.format(elapsed_time))

    if set(matches_re) != set(matches_cre):
        print('CRITICAL: (cre) and (re) generated different matches')


if __name__ == '__main__':
    demo()
