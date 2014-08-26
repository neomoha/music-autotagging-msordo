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

import os, shutil
import yaml, json
import subprocess

from unipath import Path

class DatasetCreator:
    def __init__(self, collection_name):
        self.collection_name = collection_name
    
    def __remove_temp_dirs(self):
        pass
        #shutil.rmtree("temp/")
    
    def __json2yaml(self, features_path):
        '''
        Converts json features files into yaml files, maintaining the collection's directory structure
        '''
        if not os.path.exists("temp/"):
            os.mkdir("temp/")
        if not os.path.exists("temp/"+self.collection_name):
            os.mkdir("temp/"+self.collection_name)
        for root, dirs, featurefiles in os.walk(features_path):
            for featurefile in featurefiles:
                if featurefile.endswith(".json"):
                    featurefile_path_json = root+"/"+featurefile
                    featurefile_relpath = featurefile_path_json.split(features_path+"/")[1]
                    featurefile_relpath = featurefile_relpath[:featurefile_relpath.rfind(".json")]+".sig"
                    featurefile_path_yaml = Path("temp/"+self.collection_name+"/"+featurefile_relpath)
                    print featurefile_path_yaml
                    if featurefile_path_yaml.exists():
                        continue
                    if len(featurefile_path_yaml.parent) > 0 and not os.path.exists(featurefile_path_yaml.parent):
                        os.makedirs(featurefile_path_yaml.parent)
                    features = json.load(open(featurefile_path_json))
                    yaml.dump(features, open(featurefile_path_yaml, "w"))
    
    def __create_yaml_list(self, features_file):
        if not os.path.exists("temp/"):
            os.mkdir("temp/")
        if not os.path.exists("temp/"+self.collection_name):
            os.mkdir("temp/"+self.collection_name)
        with open("temp/"+self.collection_name+"/training_features.yaml", "w") as outfile:
            with open(features_file) as infile:
                for line in infile:
                    trackid, trackpath = line.strip().split("\t")
                    outfile.write('  "%s": "%s"\n' % (trackid, trackpath))
    
    def create(self, training_features_file, chunk_size=5000, suffix=None, replace=False):
        print "Creating gaia dataset..."
        if not os.path.exists("dbs"):
            os.mkdir("dbs")
        db_file = "dbs/%s.db" % self.collection_name
        if suffix is not None:
            db_file = "dbs/%s__%s.db" % (self.collection_name, suffix)
        if os.path.exists(db_file) and replace is False:
            return 0
        #json to yaml (TODO: remove when gaiafusion accepts json files instead of yaml files)
        #self.__json2yaml(features_path)
        self.__create_yaml_list(training_features_file)
        #call gaiafusion to create dataset
        yaml_features_file = "temp/"+self.collection_name+"/training_features.yaml"
        cmd = "gaiafusion -c %d -y %s %s" % (chunk_size, yaml_features_file, db_file)
        print cmd
        code = subprocess.call(cmd.split(), stdout=subprocess.PIPE)
        if code != 0:
            print "ERROR while creating a dataset for the '%s' collection" % collection_name
        else:
            self.__remove_temp_dirs()
        return code