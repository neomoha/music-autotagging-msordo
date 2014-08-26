import os, glob

from FeatureExtractor import FeatureExtractor
from DatasetCreator import DatasetCreator
from FeatureSelector import FeatureSelector
from Autotagger import Autotagger
from validation import kfold_cross_validation
import evaluation

def _load_metadata(metadata_filename):
    metadata = dict()
    with open(metadata_filename) as f:
        for line in f:
            data = line.strip().split("\t")
            if len(data) < 3:
                print "ERROR in line %d of the metadata file %s: less than 2 values" % (i, metadata_file)
                sys.exit()
            trackid, trackpath, tag = data[:3]
            if not os.path.exists(trackpath):
                continue
            weight = 1
            if len(data) > 3:
                weight = data[3]
            metadata.setdefault(trackid, []).append((trackpath, tag, weight))
    return metadata

def _load_features(collection_name):
    features = dict()
    for ft in glob.glob(os.getcwd()+"/features/"+collection_name+"/*.sig"):
        if ft.find(".mp3.") > -1:
            k = ft[ft.rfind("/")+1:ft.rfind(".mp3")]
        else:
            k = ft[ft.rfind("/")+1:ft.rfind(".")]
        features[k] = ft
    return features

def _split_metadata_and_features(collection_name, k=5):
    metadata = _load_metadata('metadata/%s_metadata.tsv' % collection_name)
    features = _load_features(collection_name)
    idx = 1
    for train_set, test_set in kfold_cross_validation(metadata, k):
        # TRAINING SET
        if not os.path.exists("train/"):
            os.mkdir("train/")
        with open("train/%s_metadata__fold%d.tsv" % (collection_name, idx), "w") as f_meta:
            with open("train/%s_features__fold%d.tsv" % (collection_name, idx), "w") as f_feat:
                for k in train_set:
                    if k in metadata and k in features:
                        for trackpath, tag, weight in metadata[k]:
                            f_meta.write("%s\t%s\t%s\t%s\n" % (k, trackpath, tag, weight))
                        f_feat.write("%s\t%s\n" % (k, features[k]))
        # TEST SET
        if not os.path.exists("test/"):
            os.mkdir("test/")
        with open("test/%s_metadata__fold%d.tsv" % (collection_name, idx), "w") as f_meta:
            with open("test/%s_features__fold%d.tsv" % (collection_name, idx), "w") as f_feat:
                for k in test_set:
                    if k in metadata and k in features:
                        for trackpath, tag, weight in metadata[k]:
                            f_meta.write("%s\t%s\t%s\t%s\n" % (k, trackpath, tag, weight))
                        f_feat.write("%s\t%s\n" % (k, features[k]))
        idx += 1

def feature_extraction(collection_name):
    '''
    Extract features for all the songs of the collection
    Change path_to_extractor and path_to_audio accordingly
    '''
    print "----------------------- FEATURE EXTRACTION -----------------------"
    path_to_extractor='/path/to/essentia-2.0.1/build/src/examples/streaming_extractor_archivemusic'
    path_to_audio='/path/to/audio'
    path_to_features='features/%s' % collection_name
    replace_features=False
    extractor = FeatureExtractor(path_to_extractor)
    extractor.extract(path_to_audio, path_to_features, replace_features=replace_features)

def training_and_classification_with_kfold_cross_validation(collection_name, k):
    '''
    Training and classification of an autotagger using k-fold cross validation
    '''
    _split_metadata_and_features(collection_name, k)
    for i in range(1,k+1):
        # Create a gaia dataset with the training set
        print "----------------------- DATASET CREATION (FOLD %d)-----------------------" % i
        training_features='train/%s_features__fold%d.tsv' % (collection_name, i)
        chunk_size=5000
        dataset_suffix="fold%d" % i
        replace_dataset=True
        dataset_creator = DatasetCreator(collection_name)
        dataset_creator.create(training_features, chunk_size, dataset_suffix, replace_dataset)
            
        # Feature selection over the gaia dataset
        print "----------------------- FEATURE SELECTION (FOLD %d)-----------------------" % i
        dataset='dbs/%s__fold%d.db' % (collection_name, i)
        pca_covered_variance=75
        include_highlevel=True
        feature_selector = FeatureSelector()
        feature_selector.select(dataset, pca_covered_variance, include_highlevel)
        
        # Autotag a given test set
        print "----------------------- AUTOTAGGING (FOLD %d)-----------------------" % i
        dataset='transformed_dbs/%s__fold%d.db' % (collection_name, i)
        training_metadata='train/%s_metadata__fold%d.tsv' % (collection_name, i)
        test_features='test/%s_features__fold%d.tsv' % (collection_name, i)
        output_binary='test/%s_output_binary__fold%d.tsv' % (collection_name, i)
        output_affinity='test/%s_output_affinity__fold%d.tsv' % (collection_name, i)
        metric='LC'
        num_sim=18
        threshold=0.2
        autotagger = Autotagger()
        autotagger.train(dataset, training_metadata)
        autotagger.classify(test_features, output_binary, metric, num_sim, threshold, ranked=False)
        autotagger.classify(test_features, output_affinity, metric, num_sim, threshold, ranked=True)

def evaluation_with_kfold_cross_validation(collection_name, k):
    '''
    Evaluation of an autotagger using k-fold cross validation.
    Evaluation is averaged per fold
    '''
    for i in range(1,k+1):
        # Evaluation
        print "----------------------- EVALUATION (FOLD %d)-----------------------" % i
        test_metadata = 'test/%s_metadata__fold%d.tsv' % (collection_name, i)
        output_binary = 'test/%s_output_binary__fold%d.tsv' % (collection_name, i)
        output_affinity = 'test/%s_output_affinity__fold%d.tsv' % (collection_name, i)
        evaluation.binary_relevance_measures(test_metadata, output_binary)
        evaluation.affinity_measures(test_metadata, output_affinity)

if __name__ == '__main__':
    collection_name='majorminer'
    k = 3
    feature_extraction(collection_name) # you need to change some paths here
    training_and_classification_with_kfold_cross_validation(collection_name, k)
    evaluation_with_kfold_cross_validation(collection_name, k)
