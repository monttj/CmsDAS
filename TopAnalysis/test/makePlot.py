#! /usr/bin/env python

from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT 
from CrossSectionTable import *
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

c = TCanvas("c","c",600,600)
f_ttbar = TFile("plots_ttbar.root", "read") 
f_wjets = TFile("plots_wjets.root", "read") 
f_singletop_t = TFile("plots_singletop_t.root", "read") 
f_zjets = TFile("plots_zjets.root", "read")
f_data = TFile("plots_data.root", "read") 

h_ttbar_m3Hist = f_ttbar.Get("m3Hist")
h_wjets_m3Hist = f_wjets.Get("m3Hist")
h_singletop_t_m3Hist = f_singletop_t.Get("m3Hist")
h_zjets_m3Hist = f_zjets.Get("m3Hist")
h_data_m3Hist = f_data.Get("m3Hist")

lumi_data = 46.48  #data
lumi_ttbar = 38662 / Xsection["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"] 
lumi_wjets = 2859761 /Xsection["WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]  
lumi_singletop_t = 6322 / Xsection["ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"] 
lumi_zjets = 280051 / Xsection["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]
 
scale_ttbar = lumi_data / lumi_ttbar
scale_wjets = lumi_data / lumi_wjets
scale_singletop_t = lumi_data / lumi_singletop_t
scale_zjets = lumi_data / lumi_zjets
 
h_ttbar_m3Hist.Scale(scale_ttbar)
h_wjets_m3Hist.Scale(scale_wjets)
h_singletop_t_m3Hist.Scale(scale_singletop_t)
h_zjets_m3Hist.Scale(scale_zjets)

h_ttbar_m3Hist.SetFillColor(kRed+1)
h_wjets_m3Hist.SetFillColor(kGreen-3)
h_singletop_t_m3Hist.SetFillColor(kMagenta)
h_zjets_m3Hist.SetFillColor(kAzure-2)

s = THStack("hs","")
s.Add(h_ttbar_m3Hist)
s.Add(h_wjets_m3Hist)
s.Add(h_singletop_t_m3Hist)
s.Add(h_zjets_m3Hist)
s.Draw()
s.SetMaximum(65)
s.GetXaxis().SetTitle("M3 (GeV)")
s.GetYaxis().SetTitle("Number of Events")

h_data_m3Hist.Draw("sameP")
h_data_m3Hist.SetMarkerStyle(20)
h_data_m3Hist.SetMarkerSize(0.9)

n_ttbar = h_ttbar_m3Hist.Integral()
n_wjets = h_wjets_m3Hist.Integral()
n_singletop_t = h_singletop_t_m3Hist.Integral()
n_zjets = h_zjets_m3Hist.Integral()
n_background = n_ttbar + n_wjets + n_singletop_t + n_zjets
n_data = h_data_m3Hist.Integral()

print "wjets = " + str(n_wjets) 
print "singletop_t = " + str(n_singletop_t) 
print "zjets = " + str(n_zjets) 
print "background = " + str(n_background)
print "Data = " + str(n_data) 

l = TLegend(0.60,0.58,0.82,0.88)
l.AddEntry(h_ttbar_m3Hist,"ttbar","F")
l.AddEntry(h_wjets_m3Hist,"wjets","F")
l.AddEntry(h_singletop_t_m3Hist,"singletop","F")
l.AddEntry(h_zjets_m3Hist,"zjets","F")
l.AddEntry(h_data_m3Hist,"data","P")
l.SetTextSize(0.05);
l.SetLineColor(0);
l.SetFillColor(0);
l.Draw()

c.Print("m3Hist.png")


