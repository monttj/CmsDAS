import FWCore.ParameterSet.Config as cms

def getFileList(filelist_name) :
  ## Please, select Data sample file list.
  readfile = open(filelist_name)
  filelist =[ ]
  for file in readfile.readlines() :
    filelist.append("file:"+file)
  return filelist

process = cms.Process("JSON")

filelist_name = "../python/sourceFiles/KNU/SingleMuon.txt"
filelist = getFileList( filelist_name ) 
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       filelist
    )
)



import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = 'JSON/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_MuonPhys_v2.txt').getVLuminosityBlockRange()

## Output Module Configuration (expects a path 'p')
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('catTuple_data.root'),
    outputCommands = cms.untracked.vstring('keep *')
)

process.outpath = cms.EndPath(process.out)

