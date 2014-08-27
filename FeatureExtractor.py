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

import os, subprocess
from unipath import Path

class FeatureExtractor():
    def __init__(self, extractor):
        self.extractor = extractor 
    
    def extract(self, audio_path, features_path, audio_filetype="mp3", replace_features=False):
        for root, dirs, audiofiles in os.walk(audio_path):
            for audiofile in audiofiles:
                if audiofile.endswith(".%s" % audio_filetype):
                    audiofilename = root+"/"+audiofile
                    common_prefix = os.path.commonprefix([audiofilename, audio_path])
                    features_fullpath = Path(features_path+"/"+os.path.relpath(audiofilename, common_prefix)+".sig")
                    if os.path.exists(features_fullpath) and replace_features is False:
                        continue
                    if not os.path.exists(features_fullpath.parent):
                        os.makedirs(features_fullpath.parent)
                    cmd = "%s %s %s" % (self.extractor, audiofilename, features_fullpath)
                    print cmd
                    code = subprocess.call(cmd.split(), stdout=subprocess.PIPE)
                    if code != 0:
                        print "ERROR: extracting features for audio %s" % audiofilename
                        continue
