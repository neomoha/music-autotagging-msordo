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

import os
import gaia2

class Autotagger:
    def __init__(self):
        pass
    
    def __load_dataset(self, dataset_file):
        print "Loading training dataset...."
        self.ds = gaia2.DataSet()
        self.ds.load(dataset_file)
    
    def __load_training_metadata(self, metadata_file):
        '''
        Load training metadata
        The metadata_file should be in the format:
        trackid[TAB]trackpath[TAB]tag([TAB]weight)
        '''
        print "Loading training metadata..."
        self.metadata = dict()
        i = 1
        with open(metadata_file) as f:
            for line in f:
                data = line.strip().split("\t")
                if len(data) < 3:
                    print "ERROR in line %d of the metadata file %s: less than 3 values" % (i, metadata_file)
                    return
                trackid, trackpath, tag = data[:3]
                weight = 1
                if len(data) > 3:
                    weight = data[3]
                self.metadata.setdefault(trackid, []).append((tag, weight))
                i += 1
    
    def __get_similars(self, query_point, num_sim, metric):
        '''
        Return a list of the K nearest points (songs) to a given query point (song)
        '''
        transfop = self.ds.history().mapPoint(query_point) #Map the query point to the feature space of the annotated dataset
        # Define a gaia metric
        if metric == "LC":
            gaia_metric = gaia2.DistanceFunctionFactory.create('linearcombination', self.ds.layout(), 
                                { 'eucpca': { 'distance': 'euclidean',
                                    'weight': 0.8,
                                    'params': { 'descriptorNames': 'pca*' } },
                                'klmfcc': { 'distance': 'kullbackleibler',
                                    'weight': 0.2,
                                    'params': { 'descriptorName': 'lowlevel.mfcc' } }})
        elif metric == "EUC":
            gaia_metric = gaia2.DistanceFunctionFactory.create('euclidean', self.ds.layout(), { 'descriptorNames': 'pca*' })
        elif metric == "KL":
            gaia_metric = gaia2.DistanceFunctionFactory.create('kullbackleibler', self.ds.layout(), { 'descriptorName': 'lowlevel.mfcc' })
            
        view = gaia2.View(self.ds) 
        similar_points = view.nnSearch(transfop, gaia_metric) # search for nearest neighbors using a specific metric
        if num_sim is None:
            num_sim = self.ds.size()
        similar_points = similar_points.get(num_sim)
        return similar_points
    
    def __unranked_propagation(self, similars, threshold=None):
        tag_freq = dict()
        for similar in similars:
            trackid = similar[0]
            if trackid.endswith(".mp3"):
                trackid = trackid[:trackid.rfind(".mp3")]
            for tag, weight in self.metadata[trackid]:
                tag_freq.setdefault(tag, 0)
                tag_freq[tag] += 1
        proposed_tags = dict()
        cutoff = 1
        if threshold is not None:
            cutoff = int(round(len(similars)*threshold))
        for tag, freq in tag_freq.iteritems():
            if freq >= cutoff:
                proposed_tags[tag] = float(freq)/len(similars)
        proposed_tags = sorted(proposed_tags.items(), key=lambda x: x[1], reverse=True)
        return proposed_tags
    
    def __get_normalized_weights(self, similars, num_sim=1):
        norm_weights = []
        for i in range(1,len(similars)+1):
            if i <= num_sim:
                norm_weights.append(1.0)
            else:
                norm_weights.append(1.0/(i**2))
        return norm_weights

    def __ranked_propagation(self, similars, num_sims_cutoff=18, threshold=None):
        trackids = []
        for similar in similars:
            trackid = similar[0]
            if trackid.endswith(".mp3"):
                trackid = trackid[:trackid.rfind(".mp3")]
            trackids.append(trackid)
        
        norm_weights = self.__get_normalized_weights(similars, num_sims_cutoff) #Weighted-Vote
        tag_freq = dict()
        for i in range(len(trackids)):
            for tag, weight in self.metadata[trackids[i]]:
                tag_freq.setdefault(tag, 0)
                tag_freq[tag] += norm_weights[i]
        cutoff = 0.0
        if threshold is not None:
            cutoff = int(round(len(similars)*threshold))
        proposed_tags = [(tag, float(freq)) for tag, freq in tag_freq.iteritems() if freq >= cutoff]
        proposed_tags = sorted(proposed_tags, key=lambda x: x[1], reverse=True)
        weighting_denom = proposed_tags[0][1]
        weighted_proposed_tags = [(tag, freq/weighting_denom) for tag, freq in proposed_tags]
        return weighted_proposed_tags
    
    def __propagation(self, query_point, metric, num_sim, threshold, ranked):
        '''
        Find num_sim most similar (labeled) songs and propagate the tags of those songs to the query song.
        '''
        
        if ranked:
            similars = self.__get_similars(query_point, num_sim=None, metric=metric)
            return self.__ranked_propagation(similars, num_sims_cutoff=num_sim, threshold=None)
        else:
            similars = self.__get_similars(query_point, num_sim=num_sim, metric=metric)
            return self.__unranked_propagation(similars, threshold=threshold)

    def train(self, dataset_file, metadata_file):
        '''
        No training required for a k-nn classifier
        '''
        self.__load_dataset(dataset_file)
        self.__load_training_metadata(metadata_file)
    def classify(self, test_features_file, output_file, metric="LC", num_sim=18, threshold=.2, ranked=False):
        '''
        Weighted-vote k-nn classifier
        The test_features_file should be in the format:
        trackid[TAB]track_features_path
        '''
        print "Autotagging...(ranked=%s)" % ranked
        with open(output_file, "w") as outfile:
            with open(test_features_file) as infile:
                count = 0
                for line in infile:
                    trackid, features_filepath = line.strip().split("\t")
                    if not os.path.exists(features_filepath):
                        print "ERROR: features file '%s' not found" % features_filepath
                        continue
                    query_point = gaia2.Point()
                    query_point.load(features_filepath) 
                    query_point.setName("%s" % (trackid))
                    proposed_tags = self.__propagation(query_point, metric, num_sim, threshold, ranked)
                    for tag, freq in proposed_tags:
                        outfile.write("%s\t%s\t%s\t%s\n" % (trackid, features_filepath, tag, freq))
                    count += 1
                    if count % 100 == 0:
                        print "%d songs processed" % count 