void roofit(){


  using namespace RooFit;
  
  TFile * f_data = new TFile("plots_data.root");
  TFile * f_ttbar = new TFile("plots_ttbar.root");
  TFile * f_zjets = new TFile("plots_zjets.root");
  TFile * f_wjets = new TFile("plots_wjets.root");
  TFile * f_qcd = new TFile("qcd_plots_data.root");
 
  TH1F * h_data = (TH1F*) f_data->Get("m3Hist"); 
  TH1F * h_ttbar = (TH1F*) f_ttbar->Get("m3Hist"); 
  TH1F * h_zjets = (TH1F*) f_zjets->Get("m3Hist"); 
  TH1F * h_wjets = (TH1F*) f_wjets->Get("m3Hist"); 
  TH1F * h_qcd = (TH1F*) f_qcd->Get("m3Hist"); 

  int nbins = h_data->GetXaxis()->GetNbins(); 
  RooRealVar x("x","x", 0, 600  ) ;

  RooDataHist data("data","data",x,h_data) ;
  RooDataHist ttbar("ttbar","ttbar",x,h_ttbar) ;
  RooDataHist zjets("zjets","zjets",x,h_zjets) ;
  RooDataHist wjets("wjets","wjets",x,h_wjets) ;
  RooDataHist qcd("qcd","qcd",x,h_qcd) ;
 
  RooHistPdf pdf_ttbar("pdf_ttbar","pdf_ttbar",x, ttbar) ; 
  RooHistPdf pdf_zjets("pdf_zjets","pdf_zjets",x, zjets) ; 
  RooHistPdf pdf_wjets("pdf_wjets","pdf_wjets",x, wjets) ; 
  RooHistPdf pdf_qcd("pdf_qcd","pdf_qcd",x, qcd) ; 

  RooRealVar nttbar("nttbar","nttbar",1300, 0, 2000);
  RooRealVar nzjets("nzjets","nzjets", 124 , 124, 124) ; //fixed 
  RooRealVar nwjets("nwjets","nwjets", 300 , 0, 1000) ; 
  RooRealVar nqcd("nqcd","nqcd", 300 , 0, 600) ; 

  RooAddPdf model("model","model",RooArgList(pdf_ttbar, pdf_zjets, pdf_wjets, pdf_qcd), RooArgList(nttbar, nzjets, nwjets, nqcd));

  RooFitResult* fitResult = model.fitTo( data );


  ///Draw
  TCanvas * c = new TCanvas("c","c",1);
  RooPlot* xframe = x.frame() ; 
  data.plotOn(xframe, DataError(RooAbsData::SumW2) );
  model.paramOn(xframe, Layout(0.65,0.9,0.9) );
  model.plotOn(xframe,Components("pdf_qcd,pdf_wjets,pdf_ttbar"),LineColor(2),FillColor(2),DrawOption("F")) ;
  model.plotOn(xframe,Components("pdf_qcd,pdf_wjets"),LineColor(3),FillColor(3),DrawOption("F")) ;
  model.plotOn(xframe,Components("pdf_qcd"),LineColor(4),FillColor(4),DrawOption("F")) ;
  model.plotOn(xframe);
  data.plotOn(xframe, DataError(RooAbsData::SumW2) ) ; 
  xframe->Draw();
}
