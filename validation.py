# -*- coding: utf-8 -*-

# This file is part of music-autotagging-msordo.
#
# music-autotagging-msordo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# music-autotagging-msordo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with music-autotagging-msordo.  If not, see <http://www.gnu.org/licenses/>.

# Written by Mohamed Sordo (@neomoha)
# Email: mohamed ^dot^ sordo ^at^ gmail ^dot^ com
# Website: http://msordo.weebly.com

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
