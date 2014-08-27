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

from Autotagger import Autotagger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Training and classification using n-fold cross_validation')
    parser.add_argument('collection_name', help='Name of the collection')
    parser.add_argument('--dataset', default=None, help='Path to the gaia dataset (default="transformed_dbs/COLLECTIONNAME.db")')
    parser.add_argument('--training-metadata', default=None, help='Metadata file for the training set (default="train/COLLECTIONNAME_metadata.txt")')
    parser.add_argument('--test-features', default=None, help='File with paths to the audio feaures of the test set (default="test/COLLECTIONNAME_features.txt")')
    parser.add_argument('--output', default=None, help='File where to store the output annotations (default="test/COLLECTIONNAME_output.txt")')
    parser.add_argument('-m', '--metric', default="LC", help='Metric to use for similarity: EUC (euclidean distance), \
                        KL (Kullback-Leibler over MFCCs features only) or LC (Linear Combination of KL and EUC) (default=LC)')
    parser.add_argument('-k', '--num-sim', type=int, default=18, help='Number of similar songs to consider (the k in k-NN) (default=18)')
    parser.add_argument('-t', '--threshold', type=float, default=0.2, help='A cutoff threshold. A tag will only be propagated to \
                        the query song if it appears in at least (k*t) songs (default=0.2)')
    parser.add_argument('-r', '--ranked-tags', help='Whether to get an affinity rank of all the tags of the collection \
                        vocabulary to each querty song (or just a list of top tags)', action="store_true")
    args = parser.parse_args()
    
    
    if args.dataset is None:
        args.dataset = "transformed_dbs/"+args.collection_name+".db"
    
    if not os.path.exists(args.dataset):
        print "Dataset '%s' not found" % args.dataset
        sys.exit(-1)
        
    if args.training_metadata is None:
        args.training_metadata = "train/"+args.collection_name+"_metadata.tsv"
    
    if not os.path.exists(args.training_metadata):
        print "Training metadata file '%s' not found" % args.training_metadata
        sys.exit(-1)
    
    if args.test_features is None:
        args.test_features = "test/"+args.collection_name+"_features.tsv"
    
    if not os.path.exists(args.test_features):
        print "Test features file '%s' not found" % args.test_features
        sys.exit(-1)
    
    if args.output is None:
        args.output = "test/"+args.collection_name+"_output.tsv"
    print args

    autotagger = Autotagger()
    autotagger.train(args.dataset, args.training_metadata)
    autotagger.classify(args.test_features, args.output, args.metric, args.num_sim, args.threshold, args.ranked_tags)
