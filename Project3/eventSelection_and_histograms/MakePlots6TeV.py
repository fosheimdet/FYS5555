import ROOT
from ROOT import *
import os, sys
# import teststat as stat
# import numpy as np

from infofile import infos

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetPadLeftMargin(0.13)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetGridStyle(2)
ROOT.gStyle.SetPadLeftMargin(0.13)
ROOT.TH1.AddDirectory(kFALSE)

channel = sys.argv[1] 


# Variables 

variables = ['pt1', 'pt2', 'eta1', 'eta2', 'phi1', 'phi2', 'mll', 'met']

xtitles = {'pt1':'Leading lepton p_{T} (GeV)', 'pt2':'Subleading lepton p_{T} (GeV)', 'eta1':'Leading lepton #eta', 'eta2':'Subleading lepton #eta', 'phi1':'Leading lepton #phi', 'phi2':'Subleading lepton #phi', 'mll':'m_{ll} (GeV)', 'met':'E_{T}^{miss} (GeV)'}


# Backgrounds

backgrounds = ['Zjets', 'Top', 'Diboson', 'Wjets'] 

Zjets = [364100, 364101, 364102, 364103, 364104, 364105, 364106, 364107, 364108, 364109, 364110, 364111, 364112, 364113, 364114, 364115, 364116, 364117, 364118, 364119, 364120, 364121, 364122, 364123, 364124, 
         364125, 364126, 364127, 364128, 364129, 364130, 364131, 364132, 364133, 364134, 364135, 364136, 364137, 364138, 364139, 364140, 364141]

Wjets = [364156, 364157, 364158, 364159, 364160, 364161, 364162, 364163, 364164, 364165, 364166, 364167, 364168, 364169, 364170, 364171, 364172, 364173, 364174, 364175, 364176, 364177, 364178, 364179, 364180, 
         364181, 364182, 364183, 364184, 364185, 364186, 364187, 364188, 364189, 364190, 364191, 364192, 364193, 364194, 364195, 364196, 364197]

Diboson = [363356, 363358, 363359, 363360, 363489, 363490, 363491, 363492, 363493]

Top = [410000, 410011, 410012, 4100013, 410014, 410025, 410026]

# Signals

signals = ['Zprime2000', 'Zprime3000', 'Zprime4000', 'Zprime5000']  #Have to be adjusted according to Z' mass

#Zprime2000 = [301215, 301220];
#Zprime3000 = [301216, 301221];
#Zprime4000 = [301217, 301222];
#Zprime5000 = [301218, 301223];

if channel == "ee":
	Zprime2000 = [301215];
	Zprime3000 = [301216];
	Zprime4000 = [301217];
	Zprime5000 = [301218];
else: 
	Zprime2000 = [301220];
	Zprime3000 = [301221];
	Zprime4000 = [301222];
	Zprime5000 = [301223];




fileIDs = {'Diboson':Diboson, 'Zjets':Zjets, 'Wjets':Wjets, 'Top':Top, 'Zprime2000':Zprime2000, 'Zprime3000':Zprime3000, 'Zprime4000':Zprime4000, 'Zprime5000':Zprime5000}  #Have to be adjusted according to Z' mass
hist_bkg = {}
for var in variables:
        hist_bkg[var] = {}
        for bkg in backgrounds:
                hist_bkg[var][bkg] = TH1F()

hist_sig = {}
for var in variables:
        hist_sig[var] = {}
        for sig in signals:
                hist_sig[var][sig] = TH1F()
                

#colours = dict(Diboson=kAzure+1, Top=kRed+1, Zjets=kOrange-2, Wjets=kGray, Zprime3000=kBlue)   #Have to be adjusted according to Z' mass
colours = dict(Diboson=kAzure+1, Top=kRed+1, Zjets=kOrange-2, Wjets=kGray, Zprime2000=kBlue,  Zprime3000=kBlack,  Zprime4000=kSpring,  Zprime5000=kTeal)
# kWhite  = 0,   kBlack  = 1,   kGray    = 920,  kRed    = 632,  kGreen  = 416,
# kBlue   = 600, kYellow = 400, kMagenta = 616,  kCyan   = 432,  kOrange = 800,
# kSpring = 820, kTeal   = 840, kAzure   =  860, kViolet = 880,  kPink   = 900

# Extract info about cross section and sum of weights from infofile 

info = {} 
for key in infos.keys(): 
        ID = infos[key]['DSID']
        info[ID] = {} 
        info[ID]['xsec'] = infos[key]['xsec'] 
        info[ID]['sumw'] = infos[key]['sumw'] 
        info[ID]['events'] = infos[key]['events']


# Function for making histograms

L = 10.6 # integrated luminosity = 10.6 fb^-1 or 10.06?
    
def fill_hist(h, h_name, key, ID):
 
    h_midl = infile.Get(h_name).Clone("h_midl") #The histogram is specified by the TFile infile (the var, bkg and ID). h_name is a title, it describes the channel and var (but not ID)

    xsec = 1000*info[ID]['xsec']
    nev = info[ID]['sumw'] 
    
    N_mc = xsec*L

    sf = N_mc/nev # We need to scale the simulated MC background to the number of events in our dataset

    if not h.GetName():  #If the histrogram of a given variable has not been filled before
        h=infile.Get(h_name)  
        h.Scale(sf)
        n = h.GetNbinsX()
        for i in range(n):
            bc = h.GetBinContent(i)
            if bc < 0: 
                h.SetBinContent(i,0)
            h.SetFillColor(colours[key])
            h.SetLineColor(colours[key])
    else:
        h_midl.Scale(sf)
        n = h_midl.GetNbinsX()
        for i in range(n):
                bc = h_midl.GetBinContent(i)
                if bc < 0: 
                    h_midl.SetBinContent(i,0) 
        h.Add(h_midl)
    return h  


# Loop over files in MC directory  

for filename in os.listdir('Histograms_article/MC/'):    #Adjust according to histogram folder
    if '.root' in filename: 
        filepath = 'Histograms_article/MC/'+filename	 #Adjust according to histogram folder
        infile = TFile(filepath)
        file_id = int(filename.split('.')[2])
        #print filename
        for var in variables:     #Do the below for every variable
                for bkg in backgrounds:
                        if file_id in fileIDs[bkg]: 
                                hist_bkg[var][bkg] = fill_hist(hist_bkg[var][bkg], 'h_'+channel+'_'+var, bkg, file_id)
                for sig in signals:
                        if file_id in fileIDs[sig]: 
                                hist_sig[var][sig] = fill_hist(hist_sig[var][sig], 'h_'+channel+'_'+var, sig, file_id)


# Get data 
    
data = TFile('Histograms_article/Data/hist.Data.2016.root')	 #Adjust according to histogram folder
hist_d ={}

for var in variables:
        hist_d[var] = data.Get('h_'+channel+'_'+var) 
        hist_d[var].SetMarkerStyle(20)
        hist_d[var].SetMarkerSize(0.7)
        hist_d[var].SetLineColor(kBlack)
        hist_d[var].GetYaxis().SetTitle("Events")
        hist_d[var].GetXaxis().SetTitle(xtitles[var]) 
        hist_d[var].GetXaxis().SetTitleFont(43)
        hist_d[var].GetXaxis().SetTitleSize(16)
        hist_d[var].GetYaxis().SetTitleFont(43)
        hist_d[var].GetYaxis().SetTitleSize(16)
        hist_d[var].GetXaxis().SetLabelFont(43)
        hist_d[var].GetXaxis().SetLabelSize(16)
        hist_d[var].GetYaxis().SetLabelFont(43)
        hist_d[var].GetYaxis().SetLabelSize(16)
        hist_d[var].GetXaxis().SetTitleOffset(4)
        hist_d[var].GetYaxis().SetTitleOffset(1.5)
        if var=='mll':
            hist_d[var].GetXaxis().SetRangeUser(225.,6000.)

        
# Style histograms, make stack and histograms with full background

stack = {} 
hist_r = {} #Histogram for the data to background ratio to be plotted at the bottom
hist_mc = {}

for var in variables:
        stack[var] = THStack(var, "")  
        hist_mc[var] = TH1F()
        hist_r[var] = TH1F()
        for bkg in reversed(backgrounds): 
                hist_bkg[var][bkg].GetYaxis().SetTitle("Events")
                hist_bkg[var][bkg].GetXaxis().SetTitle(xtitles[var]) 
                hist_bkg[var][bkg].GetXaxis().SetTitleFont(43)
                hist_bkg[var][bkg].GetXaxis().SetTitleSize(16)
                hist_bkg[var][bkg].GetYaxis().SetTitleFont(43)
                hist_bkg[var][bkg].GetYaxis().SetTitleSize(16)
                hist_bkg[var][bkg].GetXaxis().SetLabelFont(43)
                hist_bkg[var][bkg].GetXaxis().SetLabelSize(16)
                hist_bkg[var][bkg].GetYaxis().SetLabelFont(43)
                hist_bkg[var][bkg].GetYaxis().SetLabelSize(16)
                hist_bkg[var][bkg].GetXaxis().SetTitleOffset(4)
                hist_bkg[var][bkg].GetYaxis().SetTitleOffset(1.5)
                if var == 'mll':
                    hist_bkg[var][bkg].GetXaxis().SetRangeUser(225., 6000.)
                stack[var].Add(hist_bkg[var][bkg])
                if not hist_mc[var].GetName():
                    hist_mc[var] = hist_bkg[var][bkg].Clone()
                else:
                    hist_mc[var].Add(hist_bkg[var][bkg])
                    hist_r[var] = hist_d[var].Clone()
                    hist_r[var].Divide(hist_mc[var])
                    hist_r[var].SetTitle("")
                    hist_r[var].GetXaxis().SetTitle(xtitles[var])
                    hist_r[var].GetYaxis().SetTitle("Data/#SigmaMC")
                    hist_r[var].GetYaxis().SetNdivisions(506)
                    hist_r[var].SetMarkerStyle(20)
                    hist_r[var].SetMarkerSize(0.7)
                    if var=='mll':
                        hist_r[var].GetXaxis().SetRangeUser(225.,6000.)


# Make plot legend 

leg = TLegend(0.70,0.50,0.88,0.88)
leg.SetFillStyle(4000)
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.SetBorderSize(0)

bkg_labels = {'Zjets':'Z+jets', 'Top':'Top', 'Diboson':'Diboson', 'Wjets':'W+jets'}

sig_labels = {'Zprime2000':"Z' (2 TeV)",'Zprime3000':"Z' (3 TeV)",'Zprime4000':"Z' (4 TeV)", 'Zprime5000':"Z' (5 TeV)" }

for bkg in backgrounds: 
        leg.AddEntry(hist_bkg['pt1'][bkg], bkg_labels[bkg], "f")

for sig in signals: 
        leg.AddEntry(hist_sig['pt1'][sig], sig_labels[sig], "f")
        
leg.AddEntry(hist_d['pt1'],"Data","ple")

selection = ""
if channel == "ee": 
        selection = "ee" 
if channel == "uu": 
        selection = "#mu#mu"
        
# Make plots 

for var in variables: 

    cnv = TCanvas("cnv_"+var,"", 500, 500)
    cnv.SetTicks(1,1)
    cnv.SetLeftMargin(0.13)
    #cnv.SetLogy()
        
    p1 = TPad("p1", "", 0, 0.35, 1, 1) 
    p2 = TPad("p2", "", 0, 0.0, 1, 0.35)

    p1.SetLogy()
    p1.SetBottomMargin(0.0)
    p1.Draw()
    p1.cd()

    stack[var].Draw("hist")
    stack[var].SetMinimum(10E-4)            #Set this to 10E-3 for ee and 10E-4 for uu
    stack[var].GetYaxis().SetTitle("Events")
    stack[var].GetYaxis().SetTitleFont(43)
    stack[var].GetYaxis().SetTitleSize(16)
    stack[var].GetYaxis().SetLabelFont(43)
    stack[var].GetYaxis().SetLabelSize(16)
    stack[var].GetYaxis().SetTitleOffset(1.5)
    if var in ['eta1', 'eta2', 'phi1', 'phi2']:
            maximum = stack[var].GetMaximum()
            stack[var].SetMaximum(maximum*10E4)

    hist_d[var].Draw("same e0")
    leg.Draw("same")

    for sig in signals:
            hist_sig[var][sig].SetFillColor(0);
            hist_sig[var][sig].Draw("same hist");
        
    s = TLatex()
    s.SetNDC(1);
    s.SetTextAlign(13);
    s.SetTextColor(kBlack);
    s.SetTextSize(0.044);
    s.DrawLatex(0.4,0.86,"#font[72]{ATLAS} Open Data");
    s.DrawLatex(0.4,0.81,"#bf{#sqrt{s} = 13 TeV,^{}%.1f^{}fb^{-1}}" % (L));
    s.DrawLatex(0.4,0.76,"#bf{"+selection+" selection}");


    p1.Update()
    p1.RedrawAxis()

    cnv.cd() # Change directory to the canvas
        
    p2.Draw() 
    p2.cd() #Change directory to pad 2

    p2.SetGridy()

    hist_r[var].SetMaximum(1.99) 
    hist_r[var].SetMinimum(0.01)
    hist_r[var].Draw("0PZ")

    p2.SetTopMargin(0)
    p2.SetBottomMargin(0.35)
    p2.Update()
    p2.RedrawAxis()

    cnv.cd() 
    cnv.Update()
    cnv.Print('Plots/'+channel+'_'+var+'.png')
    cnv.Close()

# Find number of events within a mass region
def GetNumberEvents(hist, xmin, xmax):
  # entries = np.zeros(2)
  error = ROOT.Double()

  axis = hist.GetXaxis();
  bmin = axis.FindBin(xmin);
  bmax = axis.FindBin(xmax);
  # print "Bins: ", bmin, bmax

  integral = hist.IntegralAndError(bmin,bmax, error, "");
#  integral -= hist.GetBinContent(bmin)*(xmin-axis.GetBinLowEdge(bmin))/axis.GetBinWidth(bmin);
#  integral -= hist.GetBinContent(bmax)*(axis.GetBinUpEdge(bmax)-xmax)/axis.GetBinWidth(bmax);

  # entries[0] = integral;
  # entries[1] = error;

  return integral, error

# xminA = 1400
# xmaxA = 2600

#xmin_2TeV = [1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
#xmax_2TeV = [2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]

xmin_2TeV = [1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
xmax_2TeV = [5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900]

xmin_3TeV = [1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
xmax_3TeV = [5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900]

xmin_4TeV = [1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
xmax_4TeV = [5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900]

xmin_5TeV = [1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000]
xmax_5TeV = [5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900, 5900]

#f3ee = open("binCuts_3ee.txt", "w")
#f3uu = open("binCuts_3uu.txt", "w")





#Zprime2000 = [301215, 301220];
#Zprime3000 = [301216, 301221];
#Zprime4000 = [301217, 301222];
#Zprime5000 = [301218, 301223];
#signals = ['Zprime2000', 'Zprime3000', 'Zprime4000', 'Zprime5000'] 


# print("2TeV ee peak cuts: ")

if channel == "ee":
    	fee = open("binCuts_article_ee.txt", "w")
	fee.write("2TeV ee bin cuts" +"\n")
	fee.write("xmin  xmax  sig			b	error_b 	N_obs" +"\n")
	for i in range(0,9):
	    # print("cut: ", xmin_2TeV[i], "-", xmax_2TeV[i])
	    integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_2TeV[i], xmax_2TeV[i])
	    integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_2TeV[i], xmax_2TeV[i])
	    integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime2000'], xmin_2TeV[i], xmax_2TeV[i])
	    print("2TeV cut: ", xmin_2TeV[i], xmax_2TeV[i], "sig: ", integral_sig, "error_sig: ", error_sig, "b: ", integral_b, "Error_b:" , error_b, "N_obs:  ", integral_obs)
	    fee.write(str(xmin_2TeV[i]) +"  " + str(xmax_2TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) +"\n")
	    fee.write("\t    " +"Sig_err: " +str(error_sig)+ "\n")
    	fee.write("3TeV ee bin cuts" + "\n")
    	fee.write("xmin  xmax  sig			b	error_b 	N_obs" + "\n")
	for i in range(0,9):
		print("cut: ", xmin_3TeV[i], "-", xmax_3TeV[i])
		integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_3TeV[i], xmax_3TeV[i])
		integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_3TeV[i], xmax_3TeV[i])
		integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime3000'], xmin_3TeV[i], xmax_3TeV[i])
		fee.write(str(xmin_3TeV[i]) +"  " + str(xmax_3TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) + "\n")
		fee.write( "\t    " + "Sig_err: " + str(error_sig) + "\n")
    	fee.write("4TeV ee bin cuts" + "\n")
    	fee.write("xmin  xmax  sig			b	error_b 	N_obs" + "\n")
	for i in range(0,9):
		print("cut: ", xmin_4TeV[i], "-", xmax_4TeV[i])
		integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_4TeV[i], xmax_4TeV[i])
		integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_4TeV[i], xmax_4TeV[i])
		integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime4000'], xmin_4TeV[i], xmax_4TeV[i])
		fee.write(str(xmin_4TeV[i]) +"  " + str(xmax_4TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) + "\n")
		fee.write( "\t    " + "Sig_err: " + str(error_sig) + "\n")
    	fee.write("5TeV ee bin cuts" + "\n")
    	fee.write("xmin  xmax  sig			b	error_b 	N_obs" + "\n")
	for i in range(0,9):
		print("cut: ", xmin_5TeV[i], "-", xmax_5TeV[i])
		integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_5TeV[i], xmax_5TeV[i])
		integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_5TeV[i], xmax_5TeV[i])
		integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime5000'], xmin_5TeV[i], xmax_5TeV[i])
		fee.write(str(xmin_5TeV[i]) +"  " + str(xmax_5TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) + "\n")
		fee.write( "\t    " + "Sig_err: " + str(error_sig) + "\n")
	fee.close()

if channel == "uu":
    	fuu = open("binCuts_article_uu.txt", "w")
	fuu.write("2TeV uu bin cuts" +"\n")
	fuu.write("xmin  xmax  sig			b	error_b 	N_obs" +"\n")
	for i in range(0,9):
	    # print("cut: ", xmin_2TeV[i], "-", xmax_2TeV[i])
	    integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_2TeV[i], xmax_2TeV[i])
	    integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_2TeV[i], xmax_2TeV[i])
	    integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime2000'], xmin_2TeV[i], xmax_2TeV[i])
	    print("2TeV cut: ", xmin_2TeV[i], xmax_2TeV[i], "sig: ", integral_sig, "error_sig: ", error_sig, "b: ", integral_b, "Error_b:" , error_b, "N_obs:  ", integral_obs)
	    fuu.write(str(xmin_2TeV[i]) +"  " + str(xmax_2TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) +"\n")
	    fuu.write("\t    " +"Sig_err: " +str(error_sig)+ "\n")
    	fuu.write("3TeV uu bin cuts" + "\n")
    	fuu.write("xmin  xmax  sig			b	error_b 	N_obs" + "\n")
	for i in range(0,9):
		print("cut: ", xmin_3TeV[i], "-", xmax_3TeV[i])
		integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_3TeV[i], xmax_3TeV[i])
		integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_3TeV[i], xmax_3TeV[i])
		integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime3000'], xmin_3TeV[i], xmax_3TeV[i])
		fuu.write(str(xmin_3TeV[i]) +"  " + str(xmax_3TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) + "\n")
		fuu.write( "\t    " + "Sig_err: " + str(error_sig) + "\n")
    	fuu.write("4TeV uu bin cuts" + "\n")
    	fuu.write("xmin  xmax  sig			b	error_b 	N_obs" + "\n")
	for i in range(0,9):
		print("cut: ", xmin_4TeV[i], "-", xmax_4TeV[i])
		integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_4TeV[i], xmax_4TeV[i])
		integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_4TeV[i], xmax_4TeV[i])
		integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime4000'], xmin_4TeV[i], xmax_4TeV[i])
		fuu.write(str(xmin_4TeV[i]) +"  " + str(xmax_4TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) + "\n")
		fuu.write( "\t    " + "Sig_err: " + str(error_sig) + "\n")
    	fuu.write("5TeV uu bin cuts" + "\n")
    	fuu.write("xmin  xmax  sig			b	error_b 	N_obs" + "\n")
	for i in range(0,9):
		print("cut: ", xmin_5TeV[i], "-", xmax_5TeV[i])
		integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_5TeV[i], xmax_5TeV[i])
		integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_5TeV[i], xmax_5TeV[i])
		integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime5000'], xmin_5TeV[i], xmax_5TeV[i])
		fuu.write(str(xmin_5TeV[i]) +"  " + str(xmax_5TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) + "\n")
		fuu.write( "\t    " + "Sig_err: " + str(error_sig) + "\n")
	fuu.close()

# if channel == "uu":
# 	f2uu = open("binCuts_2uu.txt", "w")
# 	f2uu.write("2TeV uu bin cuts" +"\n")
# 	f2uu.write("xmin  xmax  sig			b	error_b 	N_obs" +"\n")
# 	for i in range(0,9):
# 	    # print("cut: ", xmin_2TeV[i], "-", xmax_2TeV[i])
# 	    integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_3TeV[i], xmax_3TeV[i])
# 	    integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_3TeV[i], xmax_3TeV[i])
# 	    integral_sig, error_sig = GetNumberEvents(hist_sig['mll']['Zprime2000'], xmin_3TeV[i], xmax_3TeV[i])
# 	    print("2TeV cut: ", xmin_3TeV[i], xmax_3TeV[i], "sig: ", integral_sig, "b: ", integral_b, "Error_b:" , error_b, "N_obs:  ", integral_obs)
# 	    f2uu.write(str(xmin_2TeV[i]) +"  " + str(xmax_2TeV[i]) + "  " + str(integral_sig) + "  " + str(integral_b) + " " + str(error_b) + "  " + str(integral_obs) +"\n")
# 	f2uu.close()

   # integral_b, error_b = GetNumberEvents(hist_mc['mll'], xmin_3TeV[i], xmax_3TeV[i])
    #integral_obs, error_obs = GetNumberEvents(hist_d['mll'], xmin_2TeV[i], xmin_3TeV[i])
    #integral_sig, error_sig = GetNumberEvents(hist_d['mll'], xmin_3TeV[i], xmin_3TeV[i])
    #print("3TeV cut: ", xmin_3TeV[i], xmax_3TeV[i], "sig: ", integral_sig, "b: ", integral_b, "Error_b:" , error_b, "N_obs:  ", integral_obs)



