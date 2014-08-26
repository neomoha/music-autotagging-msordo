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