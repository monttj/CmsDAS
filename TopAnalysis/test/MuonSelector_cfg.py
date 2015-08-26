import FWCore.ParameterSet.Config as cms

def getFileList(filelist_name) :
  ## Please, select Data sample file list.
  readfile = open(filelist_name)
  filelist =[ ]
  for file in readfile.readlines() :
    filelist.append("file:"+file)
  return filelist

process = cms.Process("MuonSelectedSKIM")
filelist_name = "../python/sourceFiles/KNU/SingleMuon.txt"
filelist = getFileList( filelist_name ) 
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       filelist
    )
)

process.goodCatMuons = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("catMuons"),
    cut = cms.string("pt > 20.0")
)
process.catMuonFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodCatMuons"),
    minNumber = cms.uint32(1),
)

process.muonFilterPath = cms.Path( process.goodCatMuons* process.catMuonFilter)

## Output Module Configuration (expects a path 'p')
### Adding muonFilterPath.
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('catTuple_data_atLeast_1Muon.root'),
    outputCommands = cms.untracked.vstring( 'keep *',
                                            'drop *_*_*_MuonSelectedSKIM',
                                            ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('muonFilterPath')  
    )
)

process.outpath = cms.EndPath(process.out)

