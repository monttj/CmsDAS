#! /usr/bin/env python

from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT 
from CrossSectionTable import *
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

c = TCanvas("c","c",600,600)
f_ttbar = TFile("plots_ttbar.root", "read") 
f_wjets = TFile("plots_wjets.root", "read") 
f_singletop_t = TFile("plots_singletop_t.root", "read") 
f_antisingletop_t = TFile("plots_antisingletop_t.root", "read") 
f_zjets = TFile("plots_zjets.root", "read")
f_data = TFile("plots_data.root", "read") 

h_ttbar_metVsIso = f_ttbar.Get("metVsIso")
h_wjets_metVsIso = f_wjets.Get("metVsIso")
h_singletop_t_metVsIso = f_singletop_t.Get("metVsIso")
h_antisingletop_t_metVsIso = f_antisingletop_t.Get("metVsIso")
h_zjets_metVsIso = f_zjets.Get("metVsIso")
h_data_metVsIso = f_data.Get("metVsIso")

lumi_data = 46.48  #data
lumi_ttbar = 38662 / Xsection["TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"] 
lumi_wjets = 2859761 /Xsection["WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]  
lumi_singletop_t = 6322 / Xsection["ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] 
lumi_antisingletop_t = 3762 / Xsection["ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] 
lumi_zjets = 280051 / Xsection["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]
 
scale_ttbar = lumi_data / lumi_ttbar
scale_wjets = lumi_data / lumi_wjets
scale_singletop_t = lumi_data / lumi_singletop_t
scale_antisingletop_t = lumi_data / lumi_antisingletop_t
scale_zjets = lumi_data / lumi_zjets
 
h_ttbar_metVsIso.Scale(scale_ttbar)
h_wjets_metVsIso.Scale(scale_wjets)
h_singletop_t_metVsIso.Scale(scale_singletop_t)
h_antisingletop_t_metVsIso.Scale(scale_antisingletop_t)
h_zjets_metVsIso.Scale(scale_zjets)

h_singletop_metVsIso = h_singletop_t_metVsIso.Clone()
h_singletop_metVsIso.Add(h_antisingletop_t_metVsIso)

h_ttbar_metVsIso.SetLineColor(ROOT.kRed+1)
h_wjets_metVsIso.SetLineColor(ROOT.kGreen-3)
h_singletop_metVsIso.SetLineColor(ROOT.kMagenta)
h_zjets_metVsIso.SetLineColor(ROOT.kAzure-2)

h_data_metVsIso.Draw("box")
h_data_metVsIso.SetStats(0)
h_ttbar_metVsIso.Draw("boxsame")
h_wjets_metVsIso.Draw("boxsame")
h_singletop_metVsIso.Draw("boxsame")
h_zjets_metVsIso.Draw("boxsame")

l = TLegend(0.60,0.58,0.82,0.88)
l.AddEntry(h_ttbar_metVsIso,"ttbar","F")
l.AddEntry(h_wjets_metVsIso,"wjets","F")
l.AddEntry(h_singletop_metVsIso,"singletop","F")
l.AddEntry(h_zjets_metVsIso,"zjets","F")
l.AddEntry(h_data_metVsIso,"data","F")
l.SetTextSize(0.05);
l.SetLineColor(0);
l.SetFillColor(0);
l.Draw()

# x-axis = MET / 10 GeV , y-axis = Iso / 0.02 

isocut_low = 5 
isocut_high = 25 
metcut_low = 2 
metcut_high = 5 

nb_data = h_data_metVsIso.Integral(1,metcut_low, 1,isocut_low) # low MET, low isolation
nc_data = h_data_metVsIso.Integral(1,metcut_low, isocut_high,-1) # low MET, high isolation
nd_data = h_data_metVsIso.Integral(metcut_high,-1, isocut_high, -1) # high MET, high isolation

nb_ttbar = h_ttbar_metVsIso.Integral(1,metcut_low, 1,isocut_low) # low MET, low isolation
nc_ttbar = h_ttbar_metVsIso.Integral(1,metcut_low, isocut_high,-1) # low MET, high isolation
nd_ttbar = h_ttbar_metVsIso.Integral(metcut_high,-1, isocut_high, -1) # high MET, high isolation

nb_wjets = h_wjets_metVsIso.Integral(1,metcut_low, 1,isocut_low) # low MET, low isolation
nc_wjets = h_wjets_metVsIso.Integral(1,metcut_low, isocut_high,-1) # low MET, high isolation
nd_wjets = h_wjets_metVsIso.Integral(metcut_high,-1, isocut_high, -1) # high MET, high isolation

nb_zjets = h_zjets_metVsIso.Integral(1,metcut_low, 1,isocut_low) # low MET, low isolation
nc_zjets = h_zjets_metVsIso.Integral(1,metcut_low, isocut_high,-1) # low MET, high isolation
nd_zjets = h_zjets_metVsIso.Integral(metcut_high,-1, isocut_high, -1) # high MET, high isolation

nb_singletop = h_singletop_metVsIso.Integral(1,metcut_low, 1,isocut_low) # low MET, low isolation
nc_singletop = h_singletop_metVsIso.Integral(1,metcut_low, isocut_high,-1) # low MET, high isolation
nd_singletop = h_singletop_metVsIso.Integral(metcut_high,-1, isocut_high, -1) # high MET, high isolation

print "In data : " + "B = " + str(nb_data) + " C = " + str(nc_data) + " D = " + str(nd_data)  
print "In ttbar : " + "B = " + str(nb_ttbar) + " C = " + str(nc_ttbar) + " D = " + str(nd_ttbar)  
print "In wjets : " + "B = " + str(nb_wjets) + " C = " + str(nc_wjets) + " D = " + str(nd_wjets)  
print "In zjets : " + "B = " + str(nb_zjets) + " C = " + str(nc_zjets) + " D = " + str(nd_zjets)  
print "In singletop : " + "B = " + str(nb_singletop) + " C = " + str(nc_singletop) + " D = " + str(nd_singletop)  

nb = nb_data - nb_ttbar - nb_zjets - nb_singletop  #-nb_wjets
nc = nc_data - nc_ttbar - nc_zjets - nc_singletop  #-nc_wjets
nd = nd_data - nd_ttbar - nd_zjets - nd_singletop  #-nd_wjets

na = nb * nd/nc

print "B region = " + str(nb)
print "C region = " + str(nc)
print "D region = " + str(nd)
print "Estimated number of QCD in signal region = " + str(na)

c.Print("metVsIso.png")


