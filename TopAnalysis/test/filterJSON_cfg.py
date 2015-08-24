import FWCore.ParameterSet.Config as cms

process = cms.Process("JSON")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       # at KISTI 
       'file:/cms/scratch/CAT/SingleMuon/v7-3-0_Run2015B-PromptReco-v1/150720_060727/0000/catTuple_4.root',
       'file:/cms/scratch/CAT/SingleMuon/v7-3-0_Run2015B-PromptReco-v1/150720_060727/0000/catTuple_2.root',
       'file:/cms/scratch/CAT/SingleMuon/v7-3-0_Run2015B-PromptReco-v1/150720_060727/0000/catTuple_1.root',
       'file:/cms/scratch/CAT/SingleMuon/v7-3-0_Run2015B-PromptReco-v1/150720_060727/0000/catTuple_3.root'
    )
)



import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = 'Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_MuonPhys_v2.txt').getVLuminosityBlockRange()

## Output Module Configuration (expects a path 'p')
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('catTuple_data.root'),
    outputCommands = cms.untracked.vstring('keep *')
)

process.outpath = cms.EndPath(process.out)

