import os, sys, argparse
from FeatureExtractor import FeatureExtractor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract audio features for the collection')
    parser.add_argument('collection_name', help='Name of the collection')
    parser.add_argument('extractor', help='Path to the Essentia extractor')
    parser.add_argument('--path-to-audio', default=None, help='Path to the audio files of the collection (default="audio/COLLECTIONNAME")')
    parser.add_argument('--path-to-features', default=None, help='Path to where to store the audio features (default="features/COLLECTIONNAME")')
    parser.add_argument('-f', '--audio_filetype', default="mp3", help='Audio file type (default=mp3)')
    parser.add_argument('-r', '--replace-features', help='Replace old features files', action="store_true")
    args = parser.parse_args()
    
    if not os.path.exists(args.extractor):
        print "Path to extractor '%s' not found" % args.extractor
        sys.exit(-1)
    
    if args.path_to_audio is None:
        args.path_to_audio = "audio/"+args.collection_name
    
    if args.path_to_audio.endswith("/"):
        args.path_to_audio = args.path_to_audio[:-1]
    
    if not os.path.exists(args.path_to_audio):
        print "Path to audio '%s' not found" % args.path_to_audio
        sys.exit(-1)
    
    if args.path_to_features is None:
        if not os.path.exists("features"):
            os.mkdir("features")
        args.path_to_features = "features/"+args.collection_name
    
    if args.path_to_features.endswith("/"):
        args.path_to_features = args.path_to_features[:-1]
    if not os.path.exists(args.path_to_features[:args.path_to_features.rfind("/")]):
        print "Path to features '%s' not found" % args.path_to_features
        sys.exit(-1)
    
    print args
    extractor = FeatureExtractor(args.extractor)
    extractor.extract(args.path_to_audio, args.path_to_features, args.audio_filetype, args.replace_features)