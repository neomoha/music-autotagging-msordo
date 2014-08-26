import random, math, itertools
from collections import deque

def kfold_cross_validation(metadata, k):
    songs = metadata.keys()
    random.shuffle(songs)
    songs = deque(songs)
    chunk = int(math.ceil(float(len(songs))/k))
    idx = 0
    while idx < k:
        idx += 1
        test_set = itertools.islice(songs, 0,chunk)
        train_set = itertools.islice(songs, chunk, None)
        yield train_set, test_set
        songs.rotate(chunk)
