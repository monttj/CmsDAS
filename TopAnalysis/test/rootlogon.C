{

    gROOT->SetStyle("Plain");
    gStyle->SetOptStat(1110);
    //gStyle->SetOptStat(0);
    gStyle->SetOptFit(1);
    gStyle->SetStatW(0.25);
    gStyle->SetStatH(0.15);

    gStyle->SetCanvasDefH(400);
    gStyle->SetCanvasDefW(400);

    //2D text format
    gStyle->SetPaintTextFormat("5.3f");

    // For the axis:
    gStyle->SetAxisColor(1, "XYZ");
    gStyle->SetStripDecimals(kTRUE);
    gStyle->SetTickLength(0.03, "XYZ");
    gStyle->SetNdivisions(510, "XYZ");
    gStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
    gStyle->SetPadTickY(1);

    // To make 2D contour colorful
    gStyle->SetPalette(1); 

    //gStyle->SetOptTitle(0);
    // Margins:
    gStyle->SetPadTopMargin(0.1);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetPadLeftMargin(0.15);
    gStyle->SetPadRightMargin(0.05);

    // For the axis titles:
    gStyle->SetTitleColor(1, "XYZ");
    gStyle->SetTitleFont(42, "XYZ");
    gStyle->SetTitleSize(0.06, "XYZ");
    gStyle->SetTitleXOffset(0.9);
    gStyle->SetTitleYOffset(1.1);

    // For the axis labels:
    gStyle->SetLabelColor(1, "XYZ");
    gStyle->SetLabelFont(42, "XYZ");
    gStyle->SetLabelOffset(0.007, "XYZ");
    gStyle->SetLabelSize(0.05, "XYZ");

    /*
    gStyle->SetStatFontSize(0.15);
    gStyle->SetLabelSize(0.06,"X");
    gStyle->SetLabelSize(0.06,"Y");
    gStyle->SetLabelFont(72,"xyz");
    gStyle->SetTitleW(0.50);
    gStyle->SetTitleH(0.10);
    gStyle->SetHistLineStyle(1);
    gStyle->SetHistLineWidth(2);
    gStyle->SetMarkerStyle(20);
    gStyle->SetMarkerSize(0.4);
    gStyle->SetPaperSize(15,15);
    */

    gROOT->ForceStyle();
    //TColor *titlecol= (TColor*) (gROOT->GetListOfColors()->At(38));
    //titlecol->SetRGB(64.0/255.0, 94.0/255.0, 206.0/255.0);
}
