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
HoleSizes  = [3.2, 5.1, 6.35]

HoleSizes_Err   = [0, 0, 0]

aHoleSizes  = array.array('d', HoleSizes)

aHoleSizes_Err = array.array('d', HoleSizes_Err)

### Simulation Results ###
WhiteSilkScreenSim     = [34.3837, 31.845, 31.3288]
#WhiteSilkScreenSim     = [67.6188, 63.7626, 62.2263]
#WhiteSilkScreenSim     = [66.4617, 59.2, 54.279]
WhiteSilkScreenSim_Err = [0.118413, 0.110998, 0.1073]
#WhiteSilkScreenSim     = [98.35, 91.07, 81.5]
#WhiteSilkScreenSim_Err = [11.97, 12.67, 14.84]

BlackTapeSim     = [33.7933, 28.3307, 26.8419]
#BlackTapeSim     = [66.8773, 56.937, 51.1819]
#BlackTapeSim     = [63.6708, 44.0544, 36.8592]
BlackTapeSim_Err = [0.1114095, 0.0953604, 0.0810464]
#BlackTapeSim     = [48.69, 24.98, 11.75]
#BlackTapeSim_Err = [7.358, 5.03, 3.679]

NoBackBoardSim     = [33.277, 21.7144]
#NoBackBoardSim     = [33.277, 25.0815, 21.7144]
#NoBackBoardSim     = [63.6831, 42.3028, 34.9325]
NoBackBoardSim_Err = [0.118413, 0.1073]
#NoBackBoardSim_Err = [0.118413, 0.110998, 0.1073]


aWhiteSilkScreenSim     = array.array('d', WhiteSilkScreenSim)
aWhiteSilkScreenSim_Err = array.array('d', WhiteSilkScreenSim_Err)
aBlackTapeSim     = array.array('d', BlackTapeSim)
aBlackTapeSim_Err = array.array('d', BlackTapeSim_Err)
aNoBackBoardSim    = array.array('d', NoBackBoardSim)
aNoBackBoardSim_Err = array.array('d', NoBackBoardSim_Err)

### Data Results ###
ErrorHi = 0.071
ErrorLo = 0.014
#WhiteSilkScreen_1     = [34.69, 33.77, 34.01]
WhiteSilkScreen_1     = [36.26, 34.05, 33.38]
WhiteSilkScreenErrHi_1  = ErrorHi*np.array(WhiteSilkScreen_1)
WhiteSilkScreenErrLo_1  = ErrorLo*np.array(WhiteSilkScreen_1)

aWhiteSilkScreen_1      = array.array('d', WhiteSilkScreen_1)
aWhiteSilkScreenErrHi_1 = array.array('d', WhiteSilkScreenErrHi_1)
aWhiteSilkScreenErrLo_1 = array.array('d', WhiteSilkScreenErrLo_1)

#BlackTape_1     = [33.55, 30.76, 27.25]
BlackTape_1     = [35.99, 30.56, 27.62]
BlackTapeErrHi_1  = ErrorHi*np.array(BlackTape_1)
BlackTapeErrLo_1  = ErrorLo*np.array(BlackTape_1)
aBlackTape_1    = array.array('d', BlackTape_1)
aBlackTapeErrHi_1 = array.array('d', BlackTapeErrHi_1)
aBlackTapeErrLo_1 = array.array('d', BlackTapeErrLo_1)

WhiteSilkScreen_2     = [35.52, 34.37, 33.23]
WhiteSilkScreenErrHi_2  = ErrorHi*np.array(WhiteSilkScreen_2)
WhiteSilkScreenErrLo_2  = ErrorLo*np.array(WhiteSilkScreen_2)
aWhiteSilkScreen_2    = array.array('d', WhiteSilkScreen_2)
aWhiteSilkScreenErrLo_2 = array.array('d', WhiteSilkScreenErrLo_2)
aWhiteSilkScreenErrHi_2 = array.array('d', WhiteSilkScreenErrHi_2)

BlackTape_2     = [30.13, 29.97, 26.36]
BlackTapeErrLo_2  = ErrorLo*np.array(BlackTape_2)
BlackTapeErrHi_2  = ErrorHi*np.array(BlackTape_2)
aBlackTape_2    = array.array('d', BlackTape_2)
aBlackTapeErrLo_2 = array.array('d', BlackTapeErrLo_2)
aBlackTapeErrHi_2 = array.array('d', BlackTapeErrHi_2)

JulyTestbeamSizes  = [3.3, 6.35]
JulyTestbeamMPV    = [41.7, 32.0]
#JulyTestbeamSizes  = [1.8, 3.2, 7.4]
#JulyTestbeamMPV    = [35.5, 33.2, 23.8]
aJulyTestbeamErrLo   = ErrorLo*np.array(JulyTestbeamMPV)
aJulyTestbeamErrHi   = ErrorHi*np.array(JulyTestbeamMPV)

aJulyTestbeamSizes = array.array('d', JulyTestbeamSizes)
aJulyTestbeamMPV   = array.array('d', JulyTestbeamMPV)


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
	Error = (aWhiteSilkScreen_1[i]/aWhiteSilkScreenSim[i])*math.sqrt((((aWhiteSilkScreenErrLo_1[i]+aWhiteSilkScreenErrHi_1[i])/2)/aWhiteSilkScreen_1[i])**2 + (aWhiteSilkScreenSim_Err[i]/aWhiteSilkScreenSim[i])**2)
	normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormWhite = fit.GetParameter(0)
    #NormWhite = 0.548
    print "Norm: ", NormWhite
    for i in range(0, len(aWhiteSilkScreenSim)):
	aWhiteSilkScreenSim[i] = aWhiteSilkScreenSim[i]*NormWhite
    	aWhiteSilkScreenSim_Err[i] = aWhiteSilkScreenSim_Err[i]*NormWhite

    normGraph = r.TH1F("normGraph","normGraph",len(aBlackTape_1), 0, 1)

    for i in range(0, len(aBlackTapeSim)):
        normGraph.SetBinContent(i+1, aBlackTape_1[i]/aBlackTapeSim[i])
        Error = (aBlackTape_1[i]/aBlackTapeSim[i])*math.sqrt((((aBlackTapeErrLo_1[i] + aBlackTapeErrHi_1[i])/2)/aBlackTape_1[i])**2 + (aBlackTapeSim_Err[i]/aBlackTapeSim[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormBlack = fit.GetParameter(0)
    print "Norm: ", NormBlack
    print "Norm: ", NormWhite
    for i in range(0, len(aBlackTapeSim)):
#        aBlackTapeSim[i] = aBlackTapeSim[i]*NormWhite
#        aBlackTapeSim_Err[i] = aBlackTapeSim_Err[i]*NormWhite
        aBlackTapeSim[i] = aBlackTapeSim[i]*NormBlack
        aBlackTapeSim_Err[i] = aBlackTapeSim_Err[i]*NormBlack


    normGraph = r.TH1F("normGraph","normGraph",len(aNoBackBoardSim), 0, 1)

    for i in range(0, len(aNoBackBoardSim)):
        normGraph.SetBinContent(i+1, aJulyTestbeamMPV[i]/aNoBackBoardSim[i])
        Error = (aJulyTestbeamMPV[i]/aNoBackBoardSim[i])*math.sqrt((((aJulyTestbeamErrLo[i] + aJulyTestbeamErrHi[i])/2)/aJulyTestbeamMPV[i])**2 + (aNoBackBoardSim_Err[i]/aNoBackBoardSim[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    NormNoBackBoard = fit.GetParameter(0)
    print "NormNoBackBoard: ", NormNoBackBoard
    for i in range(0, len(aNoBackBoardSim)):
	aNoBackBoardSim[i] = aNoBackBoardSim[i]*NormNoBackBoard
	aNoBackBoardSim_Err[i] = aNoBackBoardSim_Err[i]*NormNoBackBoard


elif Samples == "2":
    normGraph = r.TH1F("normGraph","normGraph",len(aWhiteSilkScreen_2), 0, 1)

    for i in range(0, len(aWhiteSilkScreenSim)):
        normGraph.SetBinContent(i+1, aWhiteSilkScreen_2[i]/aWhiteSilkScreenSim[i])
        Error = (aWhiteSilkScreen_2[i]/aWhiteSilkScreenSim[i])*math.sqrt((((aWhiteSilkScreenErrLo_2[i] + aWhiteSilkScreenErrHi_2[i])/2)/aWhiteSilkScreen_2[i])**2 + (aWhiteSilkScreenSim_Err[i]/aWhiteSilkScreenSim[i])**2)
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
        Error = (aBlackTape_2[i]/aBlackTapeSim[i])*math.sqrt((((aBlackTapeErrLo_2[i] + aBlackTapeErrHi_2[i])/2)/aBlackTape_2[i])**2 + (aBlackTapeSim_Err[i]/aBlackTapeSim[i])**2)
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
    grData_White = r.TGraphAsymmErrors(len(aHoleSizes), aHoleSizes, aWhiteSilkScreen_1, aHoleSizes_Err, aHoleSizes_Err, aWhiteSilkScreenErrLo_1, aWhiteSilkScreenErrHi_1)
    grSimulation_Black = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aBlackTapeSim,aHoleSizes_Err,aBlackTapeSim_Err)
    grData_Black = r.TGraphAsymmErrors(len(aHoleSizes), aHoleSizes, aBlackTape_1, aHoleSizes_Err, aHoleSizes_Err, aBlackTapeErrLo_1, aBlackTapeErrHi_1)
    grData_July  = r.TGraphAsymmErrors(len(aJulyTestbeamSizes), aJulyTestbeamSizes, aJulyTestbeamMPV, aHoleSizes_Err, aHoleSizes_Err, aJulyTestbeamErrLo, aJulyTestbeamErrHi)
    grSimulation_NoBackBoard = r.TGraphErrors(len(aJulyTestbeamSizes),aJulyTestbeamSizes,aNoBackBoardSim,aHoleSizes_Err,aNoBackBoardSim_Err)


elif Samples == "2":
    grSimulation_White = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aWhiteSilkScreenSim,aHoleSizes_Err,aWhiteSilkScreenSim_Err)
    grMax = r.TMath.MaxElement(grSimulation_White.GetN(),grSimulation_White.GetY())
    grData_White = r.TGraphAsymmErrors(len(aHoleSizes), aHoleSizes, aWhiteSilkScreen_2, aHoleSizes_Err, aHoleSizes_Err, aWhiteSilkScreenErrLo_2, aWhiteSilkScreenErrHi_2)
    grSimulation_Black = r.TGraphErrors(len(aHoleSizes),aHoleSizes,aBlackTapeSim,aHoleSizes_Err,aBlackTapeSim_Err)
    grData_Black = r.TGraphAsymmErrors(len(aHoleSizes), aHoleSizes, aBlackTape_2, aHoleSizes_Err, aHoleSizes_Err, aBlackTapeErrLo_1, aBlackTapeErrHi_1)
    grData_July  = r.TGraphAsymmerrors(len(aJulyTestbeamSizes), aJulyTestbeamSizes, aJulyTestbeamMPV, aHoleSizes_Err, aHoleSizes_Err, aJulyTestbeamErrLo, aJulyTestbeamErrHi)



grSimulation_White.SetTitle("")
grSimulation_White.SetMarkerColor(r.kRed)
grSimulation_White.SetLineColor(r.kRed)
grSimulation_White.SetMarkerSize(2.5)
grSimulation_White.SetMarkerStyle(32)
grSimulation_White.GetXaxis().SetTitle("Dimple Diameter (mm)")
grSimulation_White.GetYaxis().SetTitle("MPV (PE)")
grSimulation_White.GetYaxis().SetRangeUser(0, 1.5*grMax)
grSimulation_White.GetXaxis().SetRangeUser(0, 7)

grSimulation_Black.SetMarkerColor(r.kBlack)
grSimulation_Black.SetLineColor(r.kBlack)
grSimulation_Black.SetMarkerSize(2.5)
grSimulation_Black.SetMarkerStyle(32)

grData_White.SetMarkerColor(r.kRed)
grData_White.SetLineColor(r.kRed)
grData_White.SetMarkerSize(2.5)
grData_White.SetMarkerStyle(8)

grData_Black.SetMarkerColor(r.kBlack)
grData_Black.SetLineColor(r.kBlack)
grData_Black.SetMarkerSize(2.5)
grData_Black.SetMarkerStyle(8)
grData_Black.SetTitle("")
grData_Black.GetXaxis().SetTitle("Hole Diameter (mm)")
grData_Black.GetYaxis().SetTitle("MPV (PE)")
grData_Black.GetYaxis().SetRangeUser(25., 1.4*grMax)
grData_Black.GetYaxis().SetTitleOffset(0.8)

grData_July.SetTitle("")
grData_July.GetXaxis().SetTitle("Hole Diameter (mm)")
grData_July.GetYaxis().SetTitle("MPV (PE)")
grData_July.GetYaxis().SetRangeUser(20., 1.3*grMax)
grData_July.SetMarkerColor(r.kGreen)
grData_July.SetLineColor(r.kGreen)
grData_July.SetMarkerSize(2.5)
grData_July.SetMarkerStyle(8)

grSimulation_NoBackBoard.SetMarkerColor(r.kGreen)
grSimulation_NoBackBoard.SetLineColor(r.kGreen)
grSimulation_NoBackBoard.SetMarkerSize(2.5)
grSimulation_NoBackBoard.SetMarkerStyle(32)

c = r.TCanvas("c","c",1000,800)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetBorderSize(2)
c.SetFrameBorderMode(0)

CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()

#grData_July.Draw("AP")
#grSimulation_White.Draw("P same")
#grSimulation_White.Draw("AP")
#grSimulation_Black.Draw("P same")
#grData_Black.Draw("P same")
grData_Black.Draw("AP")
grData_White.Draw("P same")
grSimulation_White.Draw("P same")
grSimulation_Black.Draw("P same")
grData_July.Draw("P same")
grSimulation_NoBackBoard.Draw("P same")

CMS_lumi.CMS_lumi(c, iPeriod, iPos)

legend = r.TLegend(0.55,0.75,0.98,0.95)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
legend.SetTextFont(42)

legend2 = r.TLegend(0.16,0.75,0.52,0.95)
legend2.SetFillStyle(0)
legend2.SetBorderSize(0)
legend2.SetTextSize(0.04)
legend2.SetTextFont(42)


legend2.AddEntry(grSimulation_White, "Simulation WSS", "PE")
legend2.AddEntry(grData_White, "Data WSS", "PE")
legend.AddEntry(grSimulation_Black, "Simulation Black Tape", "PE")
legend.AddEntry(grData_Black, "Data Black Tape", "PE")
legend.AddEntry(grData_July, "Data No Back-plane", "PE")
legend2.AddEntry(grSimulation_NoBackBoard, "Sim No Back-plane", "PE")

legend.Draw("same")
legend2.Draw("same")

#CMS_lumi.CMS_lumi(c, iPeriod, iPos)
#c.cd()
#c.Update()
#c.RedrawAxis()
#frame = c.GetFrame()
#frame.Draw()

c.SaveAs("Data_vs_Simulation_HoleSize_" + Samples +".pdf")
#c.SaveAs("Data_vs_Simulation_HoleSize_" + Samples +".png")
