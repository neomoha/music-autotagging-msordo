# -*- coding: utf-8 -*-

# Copyright © <2014>  Music Technology Group - Universitat Pompeu Fabra
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

import os, sys, argparse

from FeatureSelector import FeatureSelector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Feature selection over the Gaia dataset')
    parser.add_argument('collection_name', help='Name of the collection')
    parser.add_argument('--dataset', default=None, help='Path to the gaia dataset (default="dbs/COLLECTIONNAME.db")')
    parser.add_argument('--pca-covered-variance', type=int, default=75, help='The PCA transformation should keep at least this percentage of variance (default=75)')
    parser.add_argument('--exclude-highlevel', help='exclude high level descriptors', action="store_true")
    args = parser.parse_args()
    
    if args.dataset is None:
        args.dataset = "dbs/"+args.collection_name+".db"
    
    if not os.path.exists(args.dataset):
        print "Dataset '%s' not found" % args.dataset
        sys.exit(-1)
    
    print args

    feature_selector = FeatureSelector()
    feature_selector.select(args.dataset, args.pca_covered_variance, not args.exclude_highlevel)
