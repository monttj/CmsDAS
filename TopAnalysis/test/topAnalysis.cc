#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/ChainEvent.h"
#include "CATTools/DataFormats/interface/Muon.h"
#include "CATTools/DataFormats/interface/Electron.h"
#include "CATTools/DataFormats/interface/Jet.h"
#include "CATTools/DataFormats/interface/MET.h"
#include "TROOT.h"
#include "TFile.h"
#include "TStopwatch.h"
#include "TH1F.h"
#include "TH2F.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace fwlite;
using namespace std;
const double pi = TMath::Pi();

void topAnalysis(std::string fileNamesIn, std::string outputFile="top_fwlite.root",
                 bool doMC=false, int lepType=0,
                 bool invertMET=false, bool invertPFIso=false,
                 int maxEvents=100000000)
{
  gROOT->Macro("rootlogon.C");

  TFile* f = TFile::Open("out.root", "recreate");
  f->cd();

  // Book histograms
  auto secvtxMassHist = new TH1F("secvtxMassHist", "Secondary Vertex Mass", 150, 0., 5.0);
  auto secvtxMassHistB = new TH1F("secvtxMassHistB", "Secondary Vertex Mass, b", 150, 0., 5.0);
  auto secvtxMassHistC = new TH1F("secvtxMassHistC", "Secondary Vertex Mass, c", 150, 0., 5.0);
  auto secvtxMassHistL = new TH1F("secvtxMassHistL", "Secondary Vertex Mass, usdg", 150, 0., 5.0);
  auto metVsIso = new TH2F("metVsIso", "MET Versus PFIsolation", 15, 0., 150., 200, 0., 4.0);
  auto jetPtHist = new TH1F("jetPtHist", "Jet p_{T}", 150, 0., 600.);
  auto m3Hist = new TH1F("m3Hist", "M3 Histogram", 150, 0., 600.);
  auto nJetsHist = new TH1F("nJetsHist","Number of Jets", 10, 0, 10);

  // Kinematic cuts
  const double jetPtMin = 30., leadJetPtMin = 30.;
  const double isoMax = 0.2, ssvheCut = 1.74;
  const int minJets = 4;
  const double muonPtMin = (lepType == 0 ? 45 : 20);
  const double electronPtMin = (lepType == 0 ? 20 : 35);
  const double metMin = 20;

  std::vector<std::string> files;
  if ( fileNamesIn.rfind(".root") != std::string::npos )
  {
    files.push_back(fileNamesIn);
  }
  else
  {
    std::ifstream inputFiles(fileNamesIn);
    while ( true ) 
    {
      std::string fName;
      if ( ! (inputFiles >> fName) ) break;
      if ( fName.empty() ) continue;
      files.push_back(fName);
    }
  }
  fwlite::ChainEvent events(files);

  int nEventsAnalyzed = 0, nEventsPassed4Jets = 0, nEventsPassed1Tag = 0;
  TStopwatch timer;
  timer.Start();

  int nTotal = events.size();
  if ( nTotal > maxEvents ) {
    cout << "Sample is too large(" << nTotal << ")! number of Total event is changed to " << maxEvents << endl;
    nTotal = maxEvents;
  }
  float ipercentDoneLast = -1, sumTime = 0;
  cout << "Start looping\n";
  for ( events.toBegin(); !events.atEnd(); ++events )
  {
    if ( nEventsAnalyzed == nTotal ) break;

    ++nEventsAnalyzed;
    const double percentDone = float(nEventsAnalyzed)/float(nTotal)*100.0;
    const int ipercentDone(percentDone);
    if ( ipercentDone != ipercentDoneLast ) {
      const double sumTime = timer.RealTime();
      timer.Start();
      ipercentDoneLast = ipercentDone;
      cout << "Processing " << nEventsAnalyzed << "/" << nTotal << " : " << ipercentDone << "%\n";
    }
    
    const edm::EventBase& event(events);

    edm::Handle<std::vector<double> > puHandle;
    edm::Handle<std::vector<cat::Jet> > jetHandle;
    edm::Handle<std::vector<cat::Muon> > muonHandle;
    edm::Handle<std::vector<cat::Electron> > electronHandle;
    edm::Handle<std::vector<cat::MET> > metHandle;

    event.getByLabel(edm::InputTag("pileupWeight"), puHandle);
    event.getByLabel(edm::InputTag("catJets::CAT"), jetHandle);
    event.getByLabel(edm::InputTag("catMuons::CAT"), muonHandle);
    event.getByLabel(edm::InputTag("catElectrons::CAT"), electronHandle);
    event.getByLabel(edm::InputTag("catMETs::CAT"), metHandle);

    const double met = metHandle->at(0).pt();

    TLorentzVector lep_p4;
    int nMuon = 0, nElectron = 0;
    double lep_pt = 0, lep_eta = 0, lep_phi = 0, lep_iso = 0;
    for ( unsigned int imu = 0; imu < muonHandle->size(); ++imu ) {
      const auto& mu = muonHandle->at(imu);
      const double pt = mu.pt();
      const double eta = mu.eta();
      if ( mu.isTightMuon() and mu.pt() > muonPtMin and std::abs(eta) < 2.5 ) {
        ++nMuon;
        if ( lepType == 1 and mu.pt() > lep_pt ) {
          lep_pt = pt;
          lep_eta = eta;
          lep_phi = mu.phi();
          const double nhIso = mu.neutralHadronIso();
          const double chIso = mu.chargedHadronIso();
          const double phIso = mu.photonIso();
          const double puIso = mu.puChargedHadronIso();
          lep_iso = (chIso + max(0.0, nhIso + phIso - 0.5*puIso)) / pt;
          lep_p4.SetPxPyPzE(mu.px(), mu.py(), mu.pz(), mu.energy());
        }
      }
    }
    for  ( unsigned int iel = 0; iel < electronHandle->size(); ++iel ) {
      const auto& el = electronHandle->at(iel);
      const double pt = el.pt();
      const double eta = el.eta();
      if ( el.isPF() and el.passConversionVeto() and pt > electronPtMin and std::abs(eta) < 2.5 ) {
        ++nElectron;
        if ( lepType == 0 and pt > lep_pt ) {
          lep_pt = pt;
          lep_eta = eta;
          lep_phi = el.phi();
          const double nhIso = el.neutralHadronIso();
          const double chIso = el.chargedHadronIso();
          const double phIso = el.photonIso();
          const double puIso = el.puChargedHadronIso();
          lep_iso = (chIso + max(0.0, nhIso + phIso - 0.5*puIso)) / pt;
        }
      }
    }
    const int nLepton = nMuon + nElectron;
    if ( nLepton != 1 ) continue;
    if ( lepType == 0 and nMuon == 0 ) continue;
    if ( lepType == 1 and nElectron == 0 ) continue;

    metVsIso->Fill(met, lep_iso);

    int nbjet = 0;
    std::vector<double> jets_pt, jets_eta, jets_phi, jets_btag, jets_svMass;
    std::vector<int> jets_flav;
    double evt_maxbtag = -1, evt_svMassAtMaxbtag = -1;
    for ( unsigned int ijet = 0; ijet < jetHandle->size(); ++ijet ) {
      const auto& jet = jetHandle->at(ijet);
      const double pt = jet.pt();
      const double eta = jet.eta();
      if ( pt < 30 or std::abs(eta) > 2.5 ) continue;
      if ( std::hypot(eta-lep_eta, jet.phi()-lep_phi) < 0.4 ) continue;
      
      const double btag = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
      const int flav = (doMC ? 0 : std::abs(jet.partonFlavour()));

      jets_pt.push_back(pt);
      jets_eta.push_back(eta);
      jets_phi.push_back(jet.phi());
      jets_btag.push_back(btag);
      jets_svMass.push_back(-1);
      jets_flav.push_back(flav);

      if ( btag > 0.890 ) {
        ++nbjet;
        jets_svMass.back() = jet.vtxMass();
        if ( doMC ) {
          switch ( std::abs(flav) ) {
            case 5: secvtxMassHistB->Fill(jets_svMass.back()); break;
            case 4: secvtxMassHistC->Fill(jets_svMass.back()); break;
            default: secvtxMassHistL->Fill(jets_svMass.back()); break;
          }
        }
      }
      if ( evt_maxbtag < btag ) {
        evt_maxbtag = btag;
        evt_svMassAtMaxbtag = jets_svMass.back();
      }

      jetPtHist->Fill(pt);
      secvtxMassHist->Fill(jets_svMass.back());
    }
    const int njets = jets_pt.size();
    nJetsHist->Fill(njets);
    if ( njets < minJets ) continue;
    ++nEventsPassed4Jets;

    if ( nbjet == 0 ) continue;
    ++nEventsPassed1Tag;

    if ( invertMET and met > metMin ) continue;
    else if ( !invertMET and met < metMin ) continue;

    if ( invertPFIso and lep_iso < isoMax ) continue;
    else if ( !invertPFIso and lep_iso > isoMax ) continue;

    // Now compute m3
    const double m3 = (jetHandle->at(0).p4()+jetHandle->at(1).p4()+jetHandle->at(2).p4()).mass();
    m3Hist->Fill(m3);
  }

  f->cd();
  secvtxMassHist->Write();
  secvtxMassHistB->Write();
  secvtxMassHistC->Write();
  secvtxMassHistL->Write();

  metVsIso->Write();
  jetPtHist->Write();
  m3Hist->Write();
  nJetsHist->Write();

  f->Write();

}
