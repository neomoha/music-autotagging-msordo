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