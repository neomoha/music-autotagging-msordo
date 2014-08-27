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

import gaia2

class FeatureSelector():
    def __init__(self):
        pass
    
    def select(self, dbfile, pca_covered_variance=75, highlevel=True):
        '''
        dbfile: the path to the gaia dataset
        pca_covered_variance: the pca transofrmation should keep at least this variance
        highlevel:include high level descriptors
        '''
        if not os.path.exists("transformed_dbs"):
            os.mkdir("transformed_dbs")
        prefix = dbfile[dbfile.rfind("/")+1:dbfile.rfind(".")]
        print dbfile
        ds = gaia2.DataSet()
        ds.load(dbfile)
        cleaner = gaia2.AnalyzerFactory.create('cleaner')
        cleanDB = cleaner.analyze(ds).applyToDataSet(ds)
        
        if highlevel:
            to_remove = [ '*.dmean2', '*.dvar2', '*.min', '*.max', '*cov' ]
        else:
            to_remove = [ '.highlevel.*', '*.dmean2', '*.dvar2', '*.min', '*.max', '*cov' ]
            
        fselectDB = gaia2.transform(cleanDB, 'remove', { 'descriptorNames': to_remove })
        
        # NORMALIZE, PCA & Friends
        normalize = gaia2.AnalyzerFactory.create('normalize')
        normalizedDB = normalize.analyze(fselectDB).applyToDataSet(fselectDB)
        
        pcavar = gaia2.AnalyzerFactory.create('pca', {'coveredVariance': pca_covered_variance, 'resultName': 'pca%dtransform' % pca_covered_variance})
        pcaDB = pcavar.analyze(normalizedDB).applyToDataSet(normalizedDB)
        
        mfccDB = gaia2.transform(cleanDB, 'select', { 'descriptorNames': ['*mfcc*', '.highlevel.*', '.rhythm.bpm', '.rhythm.onset_rate'] })
        
        finalDB = gaia2.mergeDataSets(mfccDB, pcaDB)
        outfile = "transformed_dbs/" + prefix + ".db"
        finalDB.save(outfile)
