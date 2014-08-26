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