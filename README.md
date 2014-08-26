Music Autotagging using a weighted-vote Nearest Neighbor classifier
======

Code for the music autotagging algorithm developed during my [PhD Thesis](http://msordo.weebly.com/thesis.html)

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

Dependencies
------

The two main dependencies of this code are [Essentia](http://essentia.upf.edu/) and [Gaia](https://github.com/MTG/gaia), two libraries developed at the [Music Technology Group](http://mtg.upf.edu/)
of the [Universitat Pompeu Fabra](http://www.upf.edu/en/). Please check their respective websites for more information. In a few words, this code uses Essentia to extract audio features for a collection of songs,
and gaia to represent those audio features in a high dimensional space and perform operations such as dimension reduction, feature selection and similarity measurement.

In my case, I follow this steps in a Linux Ubuntu distribution 

### Installing Gaia

* sudo apt-get install build-essential libqt4-dev libyaml-dev swig python-dev pkg-config
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
  
### Installing [Unipath](https://pypi.python.org/pypi/Unipath/)
* sudo pip install unipath

How to use it
------

The code is basically divided in 5 main blocks:
* Feature extraction
* Dataset creation
* Feature selection
* Training and Classification (Autotagging)
* Evaluation

There is an [example.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/example.py) script that shows how to perform autotagging over a sample dataset
(crawled from the [majorminer](http://majorminer.org/info/intro) website), using k-fold cross validation.
This script also calculates all the evaluation measures used in the [MIREX](http://www.music-ir.org/mirex/wiki/2014:Audio_Tag_Classification) competition.

Each block may also be run separately. Each block has a running script ([feature_extraction.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/feature_extraction.py),
[dataset_creation.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/dataset_creation.py),
[feature_selection.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/feature_selection.py),
[autotagging.py](https://github.com/neomoha/music-autotagging-thesis/blob/master/autotagging.py))
with different options to customize the algorithm.