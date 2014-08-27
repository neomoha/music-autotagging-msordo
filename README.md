Music Autotagging using a weighted-vote Nearest Neighbor classifier
======

Code for the music autotagging algorithm developed during my [PhD](http://msordo.weebly.com/thesis.html)

This algorithm was submitted to the [MIREX](http://www.music-ir.org/mirex/wiki/MIREX_HOME) competition in 2011 in the [Audio Tag Classification Task](http://www.music-ir.org/mirex/wiki/2011:MIREX2011_Results)
and obtained the 3rd best result.

The code is licensed under a [GPLv3](http://www.gnu.org/copyleft/gpl.html) license, so feel free to use it, modify it and redistribute it as long as you respect the license :-)

For researchers please cite the following papers if you use this code:

    @article{sordo2012semantic,
      title={Semantic annotation of music collections: a computational approach},
      author={Sordo, Mohamed},
      year={2012},
      publisher={Universitat Pompeu Fabra}
    }

or

    @inproceedings {sordo20071,
     author = {Sordo, M. and Laurier, C. and Celma, O.},
     title = {Annotating Music Collections: How content-based similarity helps to propagate labels},
     booktitle = {Proceedings of 8th International Conference on Music Information Retrieval},
     year = {2007},
     address = {Vienna, Austria},
    }
    
If you use the sample dataset included in this repository (crawled from the [majorminer](http://majorminer.org/info/intro) website), please cite the following paper:

    @article{mandel08b,
      title = {A Web-Based Game for Collecting Music Metadata},
      author = {Michael I. Mandel and Daniel P. W. Ellis},
      journal = {Journal of New Music Research},
      year = {2008},
      volume = {37},
      number = {2},
      pages = {151--165},
      url = {http://m.mr-pc.org/work/jnmr08.pdf},
    }

Dependencies
------

The two main dependencies of this code are [Essentia](http://essentia.upf.edu/) and [Gaia](https://github.com/MTG/gaia), two libraries developed at the [Music Technology Group](http://mtg.upf.edu/)
of the [Universitat Pompeu Fabra](http://www.upf.edu/en/). Please check their respective websites for more information. In a few words, this code uses Essentia to extract audio features for a collection of songs,
and Gaia to represent those audio features in a high dimensional space, and perform operations such as dimension reduction, feature selection and similarity measurement.

In my case, I follow these steps in a Linux Ubuntu distribution:

### Installing Gaia

* sudo apt-get install build-essential libqt4-dev libyaml-dev swig python-dev pkg-config
* git clone https://github.com/MTG/gaia.git
* cd gaia/
* ./waf configure --download --with-python-bindings
* ./waf
* sudo ./waf install

### Installing Essentia

* Download [essentia v. 2.0.1](https://github.com/MTG/essentia/releases/tag/v2.0.1). This version includes pre-trained high-level classification models
for genres, moods, rhythm and instrumentation. More info [here](https://github.com/MTG/essentia/releases/tag/v2.0.1)

* Run:
  * sudo apt-get install build-essential libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev python-dev libsamplerate0-dev libtag1-dev
  * sudo apt-get install python-numpy-dev python-numpy
  * (optional, only if './waf' fails loading liblapack) sudo apt-get install --reinstall libatlas-base-dev
  * tar xzf v2.0.1.tar.gz

* Edit the streaming extractor example to output yaml files instead of json (needed by Gaia)
  * open file 'essentia-2.0.1/src/examples/streaming_extractor_archivemusic.cpp' and modify line 127:
    * outputToFile(stats, outputFilename, true); --> outputToFile(stats, outputFilename, false);

* Now go to the essentia folder ('essentia-2.0.1/') and run:
  * ./waf configure --mode=release --with-python --with-cpptests --with-examples --with-vamp
  * ./waf
  * (optional) sudo ./waf install

* Finally, copy or create a symbolic link to the pre-trained svm models, for example:
  * ln -s essentia-2.0.1/src/examples/svm_models/
  
### Installing [Unipath](https://pypi.python.org/pypi/Unipath/)
* sudo pip install unipath

How to use this code
------

The code is basically divided in 5 main blocks:
* [Feature extraction](https://github.com/neomoha/music-autotagging-thesis/blob/master/FeatureExtractor.py)
* [Dataset creation](https://github.com/neomoha/music-autotagging-thesis/blob/master/DatasetCreator.py)
* [Feature selection](https://github.com/neomoha/music-autotagging-thesis/blob/master/FeatureSelector.py)
* [Training and Classification (Autotagging)](https://github.com/neomoha/music-autotagging-thesis/blob/master/Autotagger.py)
* [Evaluation](https://github.com/neomoha/music-autotagging-thesis/blob/master/evaluation.py)

There is an [example.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/example.py) script that shows how to perform autotagging over a sample dataset
(crawled from the [majorminer](http://majorminer.org/info/intro) website), using k-fold cross validation.
This script also calculates all the evaluation measures used in the [MIREX](http://www.music-ir.org/mirex/wiki/2014:Audio_Tag_Classification) competition.
To run it, you just need to change a couple of paths in the _feature_extraction_ function.

Each block may also be run separately. Each block has a running script ([feature_extraction.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/feature_extraction.py),
[dataset_creation.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/dataset_creation.py),
[feature_selection.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/feature_selection.py),
[autotagging.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/autotagging.py))
with different options to customize the algorithm.

####Note

* The metadata files should follow this format:
  * trackid[TAB]trackpath[TAB]tag([TAB]weight)
* The feature files should follow this format:
  * trackid[TAB]track_features_path

This is already explained in the code.

If you have any doubt, please feel free to [contact me](http://msordo.weebly.com/contact.html).