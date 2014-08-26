import os, sys, argparse

from DatasetCreator import DatasetCreator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a Gaia Dataset given a list of feature files')
    parser.add_argument('collection_name', help='Name of the collection')
    parser.add_argument('--training-features', default=None, help='A file containing paths to the features of the audios used for training (default="train/COLLECTIONNAME_features.txt")')
    parser.add_argument('--chunk-size', type=int, default=5000, help='The dataset will be created in chunks of N songs at a time (default=5000)')
    parser.add_argument('--dataset-suffix', default=None, help='suffix to add to the dataset filename (useful when doing k-fold cross validation, for example) (default=None)')
    parser.add_argument('-r', '--replace-dataset', help='Replace old dataset (if it exists)', action="store_true")
    args = parser.parse_args()
    
    if args.training_features is None:
        args.training_features = "train/"+args.collection_name+"_features.tsv"
    
    if not os.path.exists(args.training_features):
        print "Taining features file '%s' not found" % args.training_features
        sys.exit(-1)
    
    print args
    dataset_creator = DatasetCreator(args.collection_name)
    dataset_creator.create(args.training_features, args.chunk_size, args.dataset_suffix, args.replace_dataset)
