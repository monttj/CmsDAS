#! /usr/bin/env python
import os
import glob
import math

from optparse import OptionParser

parser = OptionParser()


############################################
#            Job steering                  #
############################################

# Input inputFiles to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
parser.add_option('--inputFiles', metavar='F', type='string', action='store',
                  default = "",
                  dest='inputFiles',
                  help='Input files')

parser.add_option('--txtfiles', metavar='F', type='string', action='store',
                  default = "",
                  dest='txtfiles',
                  help='Input txt files')

parser.add_option("--onEOSCMS", action='store_true',
                  default=False,
                  dest='onEOSCMS',
                  help='onEOSCMS')

# Output name to use. 
parser.add_option('--outputFile', metavar='F', type='string', action='store',
                  default='top_fwlite.root',
                  dest='outputFile',
                  help='output file name')

# Using MC info or not. For MC, truth information is accessed.
parser.add_option('--doMC', metavar='F', action='store_true',
                  default=False,
                  dest='doMC',
                  help='Check MC Information')

# Which lepton type to use
parser.add_option('--lepType', metavar='F', type='int', action='store',
                  default=0,
                  dest='lepType',
                  help='Lepton type. Options are 0 = muons, 1 = electrons')

# Invert MET cut?
parser.add_option('--invertMET', action='store_true',
                  default=False,
                  dest='invertMET',
                  help='Invert MET cut')

# Invert PF isolation cut?
parser.add_option('--invertPFIso', action='store_true',
                  default=False,
                  dest='invertPFIso',
                  help='Invert PF isolation cut')


(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

#infile = open( options.inputFiles )
#infileStr = infile.read().rstrip()

#print 'Getting files from this dir: ' + infileStr

# Get the file list. 
#files = glob.glob( infileStr )

# Get the file list.
if options.inputFiles:
    files = glob.glob( options.files )
    print 'getting files', files
elif options.txtfiles:
    files = []
    with open(options.txtfiles, 'r') as input_:
        for line in input_:
            files.append(line.strip())
else:
    files = []

print 'getting files: ', files

if options.onEOSCMS:
        files = ["root://eoscms.cern.ch/eos/cms" + x for x in files]
        #print 'new files', *files, sep='\n'
        #print('new files', files[0], files[1], ..., sep='\n')

fname = options.txtfiles
fileN = fname[fname.rfind('/')+1:]

# Create the output file. 
f = ROOT.TFile(options.outputFile, "recreate")
f.cd()

# Make histograms
print "Creating histograms"
secvtxMassHist = ROOT.TH1F('secvtxMassHist', "Secondary Vertex Mass", 150, 0., 5.0)
secvtxMassHistB = ROOT.TH1F('secvtxMassHistB', "Secondary Vertex Mass, b jets", 150, 0., 5.0)
secvtxMassHistC = ROOT.TH1F('secvtxMassHistC', "Secondary Vertex Mass, c jets", 150, 0., 5.0)
secvtxMassHistL = ROOT.TH1F('secvtxMassHistL', "Secondary Vertex Mass, udsg jets", 150, 0., 5.0)
metVsIso = ROOT.TH2F('metVsIso', 'MET Versus PFIsolation', 15, 0., 150., 125, 0., 2.5)
jetPtHist = ROOT.TH1F('jetPtHist', 'Jet p_{T}', 150, 0., 600.)
m3Hist = ROOT.TH1F('m3Hist', 'M3 Histogram', 150, 0., 600.)

############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
jetPtMin = 30.0
leadJetPtMin = 30.0
isoMax = 0.2
ssvheCut = 1.74
minJets = 4

if options.lepType == 0 :
    muonPtMin = 45.0
    electronPtMin = 20.0
    metMin = 20.0
    lepStr = 'Mu'
else:
    muonPtMin = 20.0
    electronPtMin = 35.0
    metMin = 20.0
    lepStr = 'Ele'


events = Events (files)

# Make the entirety of the handles required for the
# analysis. 

puHandle         = Handle( "std::vector<double>" )
puLabel    = ( "pileupWeight",   "", "CAT" )
jetHandle         = Handle( "std::vector<cat::Jet>" )
jetLabel = ("catJets","","CAT")
muonHandle         = Handle( "std::vector<cat::Muon>" )
muonLabel = ("catMuons","","CAT")
electronHandle         = Handle( "std::vector<cat::Electron>" )
electronLabel = ("catElectrons","","CAT")
metHandle = Handle( "std::vector<cat::MET>" )
metLabel = ("catMETs","","CAT")

# Keep some timing information
nEventsAnalyzed = 0
nEventsPassed4Jets = 0
nEventsPassed1Tag = 0
timer = ROOT.TStopwatch()
timer.Start()

pairs = []

# loop over events
count = 0
ntotal = events.size()
percentDone = 0.0
ipercentDone = 0
ipercentDoneLast = -1
print "Start looping"
for event in events:
    nEventsAnalyzed += 1
    ipercentDone = int(percentDone)
    if ipercentDone != ipercentDoneLast :
        ipercentDoneLast = ipercentDone
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.0f}%'.format(
            count, ntotal, ipercentDone )
    count = count + 1
    percentDone = float(count) / float(ntotal) * 100.0


    ################################################
    #   Retrieve the jet four-vector
    #   ------------------------------------
    #      The jet 4-vectors are large and hence
    #      take a long time to read out. If you don't
    #      need the other products (eta,phi,mass of jet)
    #      then don't read them out. 
    ################################################

    ################################################
    #   Retrieve the jet vertex mass and plot the
    #   secondary vertex mass for tagged jets. 
    ################################################

    event.getByLabel( jetLabel, jetHandle )
    jets = jetHandle.product()

    # Find the njet bin we're in
    njets = 0
    # Now loop over the jets, and count tags
    ntags = 0
    jets_p4 = []
    for ijet in range( 0, len( jets ) ) :
        if jets[ijet].pt() > 30.0 :
            njets += 1
        ijetP4 = ROOT.TLorentzVector()
        ijetP4.SetPtEtaPhiM( jets[ijet].pt(), jets[ijet].eta(), jets[ijet].phi(), jets[ijet].mass() )
        jets_p4.append( ijetP4 )
        jetPtHist.Fill( jets[ijet].pt() )
        tagName = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
        if jets[ijet].bDiscriminator(tagName) > 0.890:
            ntags = ntags + 1
            jetSecvtxMass = jets[ijet].vtxMass()
            secvtxMassHist.Fill( jetSecvtxMass )
            if options.doMC :
                if abs(jets[ijet].partonFlavour()) == 5 :
                    secvtxMassHistB.Fill( jetSecvtxMass )
                elif abs(jets[ijet].partonFlavour()) == 4 :
                    secvtxMassHistC.Fill( jetSecvtxMass )
                else :
                    secvtxMassHistL.Fill( jetSecvtxMass )
 
    # We're not interested in <=4 jets
    if njets < minJets :
        continue
    nEventsPassed4Jets = nEventsPassed4Jets + 1

    if ntags > 0:
        nEventsPassed1Tag = nEventsPassed1Tag + 1
        pairs.append( [event.object().id().run(),
                        event.object().id().luminosityBlock(),
                        event.object().id().event(),
                        njets,
                        ntags] )
    else :
        continue


    ################################################
    #   Require exactly one lepton (e or mu)
    #   ------------------------------------
    #      Our ntuples have both muon and electron
    #      events, and hence we must select events
    #      based on one or the other type. 
    #      To accomplish this we check the products
    #      for the type we're currently plotting
    #      (Mu or Ele), and check if the product is
    #      present. 
    ################################################
    event.getByLabel (muonLabel, muonHandle)
    muons = muonHandle.product()
    event.getByLabel (electronLabel, electronHandle)
    electrons = electronHandle.product() 

    numMuons = len(muons)
    numElectrons = len(electrons)

    # If neither muons nor electrons are found, skip
    if numMuons == 0 and numElectrons == 0 :
        continue
    # If we are looking for muons but none are found, skip
    if options.lepType == 0 and numMuons == 0 :
        continue
    # If we are looking for electrons but none are found, skip
    if options.lepType == 1 and numElectrons == 0 :
        continue

    # keep leptons with certain pt threshold in the event
    if options.lepType == 0 and muons[0].pt() <= muonPtMin:
        continue
    if options.lepType == 1 and electrons[0].pt() <= electronPtMin:
        continue
    
    # Now get the MET
    event.getByLabel( metLabel, metHandle )
    met = metHandle.product()[0].pt()

    # Now get the PF isolation
    lepIso = -1.0
    if options.lepType == 0 :
        nhIso = muons[0].neutralHadronIso()
        chIso = muons[0].chargedHadronIso()
        phIso = muons[0].photonIso() 
        puIso = muons[0].puChargedHadronIso()  
        lepIso = (chIso + max(0.0, nhIso + phIso - 0.5*puIso)) / muons[0].pt()
    if options.lepType == 1 :
        nhIso = electrons[0].neutralHadronIso()
        chIso = electrons[0].chargedHadronIso()
        phIso = electrons[0].photonIso()        
        puIso = electrons[0].puChargedHadronIso() 
        lepIso = (chIso + max(0.0, nhIso + phIso - 0.5*puIso)) / electrons[0].pt()

    # Make a plot of the MET versus ISO for normalization purposes
    metVsIso.Fill( met, lepIso )

    # If the MET is lower than our cut, skip, unless we want it inverted
    if not options.invertMET :
        if met < metMin :
            continue
    else :
        if met > metMin :
            continue

    # If the ISO is higher than our cut, skip, unless we want it inverted
    if not options.invertPFIso :
        if lepIso > isoMax :
            continue
    else :
        if lepIso < isoMax :
            continue

    # Now compute m3
    maxPt = -1.0
    m3 = -1.0
    for ijet in range(0, len(jets_p4) ) :
        for jjet in range(ijet + 1, len(jets_p4) ) :
            for kjet in range(jjet + 1, len(jets_p4) ) :
                sumP4 = jets_p4[ijet] + jets_p4[jjet] + jets_p4[kjet]
                if sumP4.Perp() > maxPt :
                    maxPt = sumP4.Perp()
                    m3 = sumP4.M()
    if maxPt > 0.0 :
        m3Hist.Fill( m3 )

# Stop our timer
timer.Stop()

# Print out our timing information
rtime = timer.RealTime(); # Real time (or "wall time")
ctime = timer.CpuTime(); # CPU time
print("Analyzed events: {0:6d}").format(nEventsAnalyzed)
print(">=4 jet events : {0:6d}").format(nEventsPassed4Jets)
print(">=1 tag events : {0:6d}").format(nEventsPassed1Tag)
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)



f.cd()
f.Write()
f.Close()

