python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/TT_TuneCUETP8M1_13TeV-powheg-pythia8.txt --outputFile=plots_ttbar.root --doMC --maximum 38662 &
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.txt --outputFile=plots_singletop_t.root --doMC --maximum 6322 &
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.txt --outputFile=plots_antisingletop_t.root --doMC --maximum 3762 &
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.txt --outputFile=plots_singletop_tW.root --doMC --maximum 1654 &
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.txt --outputFile=plots_antisingletop_tW.root --doMC --maximum 1654 &
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.txt --outputFile=plots_wjets.root --doMC --maximum 2859761 
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.txt --outputFile=plots_zjets.root --doMC --maximum 280051 &
python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/SingleMuon.txt --outputFile=plots_data.root &

### Skimmed SingleMuon data(Muon>20GeV). Original total number of events : 3633477. It is a Real data. Do not scale this sample.
#python topAnalysis.py --inputFiles=/cmsdas/data/LongEX_top/filtered_data/SingleMuon/catTuple_data_atLeast_1Muon.root --outputFile=plots_data.root &
### Skimmed WJets MC(Muon>30GeV). Please, use total number of events : 9993300 instead of 1306559
#python topAnalysis.py --txtfiles=../python/sourceFiles/KNU/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_MuonFiltered_nevt_9993300.txt --outputFile=plots_wjets.root --doMC 
