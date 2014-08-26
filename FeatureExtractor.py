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