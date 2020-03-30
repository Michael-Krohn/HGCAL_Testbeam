import ROOT as r
import sys
import datetime
import subprocess
import os
import copy
import sets
import collections
import math
import CMS_lumi, tdrstyle
import array
import numpy as np

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 0
#iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

iPeriod = 0

### Tile Sizes ###
HoleSizes  = [6.35, 9.5, 15]

HoleSizes_Err   = [0, 0, 0]

aHoleSizes  = array.array('d', HoleSizes)

aHoleSizes_Err = array.array('d', HoleSizes_Err)

### Simulation Results ###
WhiteSilkScreenSim     = [98.35, 91.07, 81.5]
WhiteSilkScreenSim_Err = [11.97, 12.67, 14.84]

BlackTapeSim     = [48.69, 24.98, 11.75]
BlackTapeSim_Err = [7.358, 5.03, 3.679]

aWhiteSilkScreenSim     = array.array('d', WhiteSilkScreenSim)
aWhiteSilkScreenSim_Err = array.array('d', WhiteSilkScreenSim_Err)
aBlackTapeSim     = array.array('d', BlackTapeSim)
aBlackTapeSim_Err = array.array('d', BlackTapeSim_Err)

### Data Results ###
Error = 0.0176
WhiteSilkScreen_1     = [36.26, 34.05, 33.38]
WhiteSilkScreenErr_1  = Error*np.array(WhiteSilkScreen_1)
aWhiteSilkScreen_1     = array.array('d', WhiteSilkScreen_1)
aWhiteSilkScreenErr_1 = array.array('d', WhiteSilkScreenErr_1)

BlackTape_1     = [35.99, 30.56, 27.62]
BlackTapeErr_1  = Error*np.array(BlackTape_1)
aBlackTape_1    = array.array('d', BlackTape_1)
aBlackTapeErr_1 = array.array('d', BlackTapeErr_1)

WhiteSilkScreen_2     = [35.52, 34.37, 33.23]
WhiteSilkScreenErr_2  = Error*np.array(WhiteSilkScreen_2)
aWhiteSilkScreen_2    = array.array('d', WhiteSilkScreen_2)
aWhiteSilkScreenErr_2 = array.array('d', WhiteSilkScreenErr_2)

BlackTape_2     = [30.13, 29.97, 26.36]
BlackTapeErr_2  = Error*np.array(BlackTape_2)
aBlackTape_2    = array.array('d', BlackTape_2)
aBlackTapeErr_2 = array.array('d', BlackTapeErr_2)


############################################
if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print "Please use 1 or 2 as an argument, corresponding to 2 different versions of the same measurement"
    exit(0)
elif len(sys.argv) == 1:
    print "Please use 1 or 2 as an argument, corresponding to 2 different versions of the same measurement"
    exit(0)


Samples = sys.argv[1]

if Samples != "1" and Samples != "2":
    print "Please use 1 or 2 as an argument, corresponding to 2 different versions of the same measurement"
    exit(0)


### Normalizing Simulation ###
if Samples == "1":
    normGraph = r.TH1F("normGraph","normGraph",len(aWhiteSilkScreen_1), 0, 1)

    for i in range(0, len(aWhiteSilkScreenSim)):
        normGraph.SetBinContent(i+1, aWhiteSilkScreen_1[i]/aWhiteSilkScreenSim[i])
	Error = (aWhiteSilkScreen_1[i]/aWhiteSilkScreenSim[i])*math.sqrt((aWhiteSilkScreenErr_1[i]/aWhiteSilkScreen_1[i])**2 + (aWhiteSilkScreenSim_Err[i]/aWhiteSilkScreenSim[i])**2)
	normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormWhite = fit.GetParameter(0)
    print "Norm: ", NormWhite
    for i in range(0, len(aWhiteSilkScreenSim)):
	aWhiteSilkScreenSim[i] = aWhiteSilkScreenSim[i]*NormWhite
    	aWhiteSilkScreenSim_Err[i] = aWhiteSilkScreenSim_Err[i]*NormWhite

    normGraph = r.TH1F("normGraph","normGraph",len(aBlackTape_1), 0, 1)

    for i in range(0, len(aBlackTapeSim)):
        normGraph.SetBinContent(i+1, aBlackTape_1[i]/aBlackTapeSim[i])
        Error = (aBlackTape_1[i]/aBlackTapeSim[i])*math.sqrt((aBlackTapeErr_1[i]/aBlackTape_1[i])**2 + (aBlackTapeSim_Err[i]/aBlackTapeSim[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormBlack = fit.GetParameter(0)
    print "Norm: ", NormBlack
    for i in range(0, len(aBlackTapeSim)):
        aBlackTapeSim[i] = aBlackTapeSim[i]*NormBlack
        aBlackTapeSim_Err[i] = aBlackTapeSim_Err[i]*NormBlack

elif Samples == "2":
    normGraph = r.TH1F("normGraph","normGraph",len(aWhiteSilkScreen_2), 0, 1)

    for i in range(0, len(aWhiteSilkScreenSim)):
        normGraph.SetBinContent(i+1, aWhiteSilkScreen_2[i]/aWhiteSilkScreenSim[i])
        Error = (aWhiteSilkScreen_2[i]/aWhiteSilkScreenSim[i])*math.sqrt((aWhiteSilkScreenErr_2[i]/aWhiteSilkScreen_2[i])**2 + (aWhiteSilkScreenSim_Err[i]/aWhiteSilkScreenSim[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormWhite = fit.GetParameter(0)
    print "Norm: ", NormWhite
    for i in range(0, len(aWhiteSilkScreenSim)):
        aWhiteSilkScreenSim[i] = aWhiteSilkScreenSim[i]*NormWhite
        aWhiteSilkScreenSim_Err[i] = aWhiteSilkScreenSim_Err[i]*NormWhite

    normGraph = r.TH1F("normGraph","normGraph",len(aBlackTape_2), 0, 1)

    for i in range(0, len(aBlackTapeSim)):
        normGraph.SetBinContent(i+1, aBlackTape_2[i]/aBlackTapeSim[i])
        Error = (aBlackTape_2[i]/aBlackTapeSim[i])*math.sqrt((aBlackTapeErr_2[i]/aBlackTape_2[i])**2 + (aBlackTapeSim_Err[i]/aBlackTapeSim[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormBlack = fit.GetParameter(0)
    print "Norm: ", NormBlack
    for i in range(0, len(aBlackTapeSim)):
        aBlackTapeSim[i] = aBlackTapeSim[i]*NormBlack
        aBlackTapeSim_Err[i] = aBlackTapeSim_Err[i]*NormBlack

### Plotting ###
if Samples == "1":
    grSimulation_White = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aWhiteSilkScreenSim,aHoleSizes_Err,aWhiteSilkScreenSim_Err)
    grMax = r.TMath.MaxElement(grSimulation_White.GetN(),grSimulation_White.GetY())
    grData_White = r.TGraphErrors(len(aHoleSizes), aHoleSizes, aWhiteSilkScreen_1, aHoleSizes_Err, aWhiteSilkScreenErr_1)
    grSimulation_Black = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aBlackTapeSim,aHoleSizes_Err,aBlackTapeSim_Err)
    grData_Black = r.TGraphErrors(len(aHoleSizes), aHoleSizes, aBlackTape_1, aHoleSizes_Err, aBlackTapeErr_1)

elif Samples == "2":
    grSimulation_White = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aWhiteSilkScreenSim,aHoleSizes_Err,aWhiteSilkScreenSim_Err)
    grMax = r.TMath.MaxElement(grSimulation_White.GetN(),grSimulation_White.GetY())
    grData_White = r.TGraphErrors(len(aHoleSizes), aHoleSizes, aWhiteSilkScreen_2, aHoleSizes_Err, aWhiteSilkScreenErr_2)
    grSimulation_Black = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aBlackTapeSim,aHoleSizes_Err,aBlackTapeSim_Err)
    grData_Black = r.TGraphErrors(len(aHoleSizes), aHoleSizes, aBlackTape_2, aHoleSizes_Err, aBlackTapeErr_1)



grSimulation_White.SetTitle("")
grSimulation_White.SetMarkerColor(r.kRed)
grSimulation_White.SetLineColor(r.kRed)
grSimulation_White.SetMarkerSize(2.5)
grSimulation_White.SetMarkerStyle(32)
grSimulation_White.GetXaxis().SetTitle("Dimple Diameter (mm)")
grSimulation_White.GetYaxis().SetTitle("MPV (PE)")
grSimulation_White.GetYaxis().SetRangeUser(0, 1.5*grMax)

grSimulation_Black.SetMarkerColor(r.kBlue)
grSimulation_Black.SetLineColor(r.kBlue)
grSimulation_Black.SetMarkerSize(2.5)
grSimulation_Black.SetMarkerStyle(32)

grData_White.SetMarkerColor(r.kBlack)
grData_White.SetLineColor(r.kBlack)
grData_White.SetMarkerSize(2.5)
grData_White.SetMarkerStyle(8)

grData_Black.SetMarkerColor(r.kGreen)
grData_Black.SetLineColor(r.kGreen)
grData_Black.SetMarkerSize(2.5)
grData_Black.SetMarkerStyle(8)



c = r.TCanvas("c","c",1000,1000)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetBorderSize(2)
c.SetFrameBorderMode(0)

grSimulation_White.Draw("AP")
grSimulation_Black.Draw("P same")
grData_Black.Draw("P same")
grData_White.Draw("P same")

legend = r.TLegend(0.43,0.7,0.98,0.95)
legend.SetFillStyle(0)
legend.SetBorderSize(1)
legend.SetTextSize(0.045)
legend.SetTextFont(42)

legend.AddEntry(grSimulation_White, "Simulation White Silkscreen", "PE")
legend.AddEntry(grData_White, "Data White Silkscreen", "PE")
legend.AddEntry(grSimulation_Black, "Simulation Black Tape", "PE")
legend.AddEntry(grData_Black, "Data Black Tape", "PE")

legend.Draw("same")

CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()

c.SaveAs("Data_vs_Simulation_HoleSize_" + Samples +".pdf")
#c.SaveAs("Data_vs_Simulation_HoleSize_" + Samples +".png")
