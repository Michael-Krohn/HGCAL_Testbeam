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

### Returns the data/sim ratio and the data error/sim ratio ###
def getRatio(dataGraph, simGraph):

    ratio      = []
    ratioErrLo = []
    ratioErrHi = []
    zero       = []
    for i in range(0,dataGraph.GetN()):
	ratio.append(dataGraph.GetY()[i]/simGraph.GetY()[i])
	ratioErrHi.append(dataGraph.GetErrorYhigh(i)/simGraph.GetY()[i])
        ratioErrLo.append(dataGraph.GetErrorYlow(i)/simGraph.GetY()[i])
	zero.append(0.0)


    return ratio, ratioErrLo, ratioErrHi, zero

### Returns the sim errors for the ratio plot ###
def getMCratioError(simGraph):

    ratioError = []
    ratio      = []
    width      = []
    errorWidth = (simGraph.GetX()[simGraph.GetN() - 1] - simGraph.GetX()[0])/50.
    for i in range(0,simGraph.GetN()):
	ratioError.append(simGraph.GetEY()[i]/simGraph.GetY()[i])
	ratio.append(simGraph.GetY()[i]/simGraph.GetY()[i])
        width.append(errorWidth)


    aRatio      = array.array('d', ratio)
    aRatioError = array.array('d', ratioError)
    aWidth      = array.array('d', width)

    grRatio = r.TGraphErrors(simGraph.GetN(),simGraph.GetX(),aRatio,aWidth,aRatioError)

    return grRatio
    
### sets up the margins of the canvas ###
def canvas_margin(c1, c1_up, c1_down):
  c1_up.SetTopMargin( 0.07 )
  c1_up.SetBottomMargin( 0.02 )
  c1_up.SetLeftMargin( 0.15 )
  c1_up.SetRightMargin( 0.03 )

  c1_down.SetTopMargin( 0.03 )
  c1_down.SetBottomMargin( 0.4 )
  c1_down.SetLeftMargin( 0.15 )
  c1_down.SetRightMargin( 0.03 )

  c1.SetTopMargin( 0.05 )
  c1.SetBottomMargin( 0.13 )
  c1.SetRightMargin( 0.05 )
  c1.SetLeftMargin( 0.16 )

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
TyvekAreas        = [9, 16, 25]
ESR3p8Areas       = [9, 16, 25]
ESR3Areas_EJ200   = [2.3*2.3, 3*3, 3.4*3.4, 5.5*5.5]
ESR3Areas_NIU     = [3.4*3.4, 3.5*3.5, 3.7*3.7, 3.8*3.8]
ESR3Areas         = [2.3*2.3, 3*3, 3.4*3.4, 3.5*3.5, 3.7*3.7, 3.8*3.8, 5.5*5.5]

Areas3p8_Err      = [0, 0, 0]
Areas3_Err        = [0, 0, 0, 0]
Areas3All_Err     = [0, 0, 0, 0, 0, 0, 0]

aTyvekAreas        = array.array('d', TyvekAreas)
aESR3p8Areas       = array.array('d', ESR3p8Areas)
aESR3Areas         = array.array('d', ESR3Areas)
aESR3Areas_EJ200   = array.array('d', ESR3Areas_EJ200)
aESR3Areas_NIU     = array.array('d', ESR3Areas_NIU)


aAreas3p8_Err = array.array('d', Areas3p8_Err)
aAreas3_Err   = array.array('d', Areas3_Err)

### Simulation Results ###
nSimEvents = 4900.
SimVsArea_Tyvek     = [78.05, 57.14, 44.1]
SimVsArea_TyvekErr  = [11.87/math.sqrt(nSimEvents), 8.11/math.sqrt(nSimEvents), 6.75/math.sqrt(nSimEvents)]

SimVsArea_3p8ESR    = [90.51, 65.95, 51.88]
SimVsArea_3p8ESRErr = [13.32/math.sqrt(nSimEvents), 8.73/math.sqrt(nSimEvents), 7.61/math.sqrt(nSimEvents)]

SimVsArea_3ESR     = [118.244, 94.0956, 84.2592, 53.2837]
SimVsArea_3ESRErr  = [0.166518, 0.147217, 0.138715, 0.10428]

SimVsArea_3ESR_NIU     = [84.2592, 81.9827, 78.0555, 76.152]
SimVsArea_3ESRErr_NIU  = [0.138715, 0.136787, 0.131719, 0.129507]

SimVsArea_3ESR_all     = [97.17, 75.95, 67.34, 65.36, 61.91, 60.4, 41.44]
SimVsArea_3ESRErr_all  = [21.99/math.sqrt(nSimEvents), 13.81/math.sqrt(nSimEvents), 10.93/math.sqrt(nSimEvents), 10.64/math.sqrt(nSimEvents), 10.05/math.sqrt(nSimEvents), 9.84/math.sqrt(nSimEvents), 6.86/math.sqrt(nSimEvents)]


aSimVsArea_Tyvek     = array.array('d', SimVsArea_Tyvek)
aSimVsArea_TyvekErr  = array.array('d', SimVsArea_TyvekErr)
aSimVsArea_3p8ESR    = array.array('d', SimVsArea_3p8ESR)
aSimVsArea_3p8ESRErr = array.array('d', SimVsArea_3p8ESRErr)
aSimVsArea_3ESR      = array.array('d', SimVsArea_3ESR)
aSimVsArea_3ESRErr   = array.array('d', SimVsArea_3ESRErr)
aSimVsArea_3ESR_NIU      = array.array('d', SimVsArea_3ESR_NIU)
aSimVsArea_3ESRErr_NIU   = array.array('d', SimVsArea_3ESRErr_NIU)

### Data Results ###
ErrorHi = 0.071
ErrorLo = 0.014
AreaSizes_Tyvek   = [9, 16, 25]
AreaSizes_3p8ESR  = [9, 16, 25]
AreaSizes_EJ3ESR  = [2.3*2.3, 9, 3.4*3.4, 5.5*5.5]
AreaSizes_NIU3ESR = [3.4*3.4, 3.5*3.5, 3.7*3.7, 3.8*3.8]

DataVsArea_Tyvek   = [7.69, 5.65, 4.38]
DataVsArea_3p8ESR  = [25.53, 15.39, 7.47]
DataVsArea_EJ3ESR  = [39.55, 32.23, 25.97, 14.71]
DataVsArea_NIU3ESR = [19.07, 21.17, 17.32, 17.71]

DataVsArea_TyvekErrLo     = ErrorLo*np.array(DataVsArea_Tyvek)
DataVsArea_3p8ESRErrLo    = ErrorLo*np.array(DataVsArea_3p8ESR)
DataVsArea_EJ3ESRErrLo    = ErrorLo*np.array(DataVsArea_EJ3ESR)
DataVsArea_NIU3ESRErrLo   = ErrorLo*np.array(DataVsArea_NIU3ESR)

DataVsArea_TyvekErrHi     = ErrorHi*np.array(DataVsArea_Tyvek)
DataVsArea_3p8ESRErrHi    = ErrorHi*np.array(DataVsArea_3p8ESR)
DataVsArea_EJ3ESRErrHi    = ErrorHi*np.array(DataVsArea_EJ3ESR)
DataVsArea_NIU3ESRErrHi   = ErrorHi*np.array(DataVsArea_NIU3ESR)

aAreaSizes_Tyvek   = array.array('d', AreaSizes_Tyvek)
aAreaSizes_3p8ESR  = array.array('d', AreaSizes_3p8ESR)
aAreaSizes_EJ3ESR  = array.array('d', AreaSizes_EJ3ESR)
aAreaSizes_NIU3ESR = array.array('d', AreaSizes_NIU3ESR)

aDataVsArea_Tyvek   = array.array('d', DataVsArea_Tyvek)
aDataVsArea_3p8ESR  = array.array('d', DataVsArea_3p8ESR)
aDataVsArea_EJ3ESR  = array.array('d', DataVsArea_EJ3ESR)
aDataVsArea_NIU3ESR = array.array('d', DataVsArea_NIU3ESR)

aDataVsArea_TyvekErrLo   = array.array('d', DataVsArea_TyvekErrLo)
aDataVsArea_3p8ESRErrLo  = array.array('d', DataVsArea_3p8ESRErrLo)
aDataVsArea_EJ3ESRErrLo  = array.array('d', DataVsArea_EJ3ESRErrLo)
aDataVsArea_NIU3ESRErrLo = array.array('d', DataVsArea_NIU3ESRErrLo)

aDataVsArea_TyvekErrHi   = array.array('d', DataVsArea_TyvekErrHi)
aDataVsArea_3p8ESRErrHi  = array.array('d', DataVsArea_3p8ESRErrHi)
aDataVsArea_EJ3ESRErrHi  = array.array('d', DataVsArea_EJ3ESRErrHi)
aDataVsArea_NIU3ESRErrHi = array.array('d', DataVsArea_NIU3ESRErrHi)


############################################
if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print "Please use Tyvek, ESR_3p8, EJ200_3ESR, or NIU_3ESR as an argument"
    exit(0)
elif len(sys.argv) == 1:
    print "Please use Tyvek, ESR_3p8, EJ200_3ESR, or NIU_3ESR as an argument"
    exit(0)


Samples = sys.argv[1]
if Samples != "Tyvek" and Samples != "ESR_3p8" and Samples != "EJ200_3ESR" and Samples != "NIU_3ESR":
    print "Please use Tyvek, ESR_3p8, EJ200_3ESR, or NIU_3ESR as an argument"
    exit(0)


### Normalizing Simulation ###
if Samples == "Tyvek":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsArea_Tyvek), 0, 1)

    for i in range(0, len(aSimVsArea_Tyvek)):
        normGraph.SetBinContent(i+1, aDataVsArea_Tyvek[i]/aSimVsArea_Tyvek[i])
	Error = (aDataVsArea_Tyvek[i]/aSimVsArea_Tyvek[i])*math.sqrt((((aDataVsArea_TyvekErrLo[i] + aDataVsArea_TyvekErrHi[i])/2)/aDataVsArea_Tyvek[i])**2 + (aSimVsArea_TyvekErr[i]/aSimVsArea_Tyvek[i])**2)
	normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsArea_Tyvek)):
	aSimVsArea_Tyvek[i] = aSimVsArea_Tyvek[i]*Norm
    	aSimVsArea_TyvekErr[i] = aSimVsArea_TyvekErr[i]*Norm
elif Samples == "ESR_3p8":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsArea_3p8ESR), 0, 1)

    for i in range(0, len(aSimVsArea_3p8ESR)):
        normGraph.SetBinContent(i+1, aDataVsArea_3p8ESR[i]/aSimVsArea_3p8ESR[i])
	Error = (aDataVsArea_3p8ESR[i]/aSimVsArea_3p8ESR[i])*math.sqrt((((aDataVsArea_3p8ESRErrLo[i] + aDataVsArea_3p8ESRErrHi[i])/2)/aDataVsArea_3p8ESR[i])**2 + (aSimVsArea_3p8ESRErr[i]/aSimVsArea_3p8ESR[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsArea_3p8ESR)):
        aSimVsArea_3p8ESR[i] = aSimVsArea_3p8ESR[i]*Norm
        aSimVsArea_3p8ESRErr[i] = aSimVsArea_3p8ESRErr[i]*Norm
elif Samples == "EJ200_3ESR":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsArea_EJ3ESR), 0, 1)

    for i in range(0, len(aSimVsArea_3ESR)):
	normGraph.SetBinContent(i+1, aDataVsArea_EJ3ESR[i]/aSimVsArea_3ESR[i])
        Error = (aDataVsArea_EJ3ESR[i]/aSimVsArea_3ESR[i])*math.sqrt((((aDataVsArea_EJ3ESRErrLo[i] + aDataVsArea_EJ3ESRErrHi[i])/2)/aDataVsArea_EJ3ESR[i])**2 + (aSimVsArea_3ESRErr[i]/aSimVsArea_3ESR[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsArea_3ESR)):
        aSimVsArea_3ESR[i] = aSimVsArea_3ESR[i]*Norm
        aSimVsArea_3ESRErr[i] = aSimVsArea_3ESRErr[i]*Norm
elif Samples == "NIU_3ESR":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsArea_NIU3ESR), 0, 1)

    for i in range(0, len(aSimVsArea_3ESR_NIU)):
        normGraph.SetBinContent(i+1, aDataVsArea_NIU3ESR[i]/aSimVsArea_3ESR_NIU[i])
        Error = (aDataVsArea_NIU3ESR[i]/aSimVsArea_3ESR_NIU[i])*math.sqrt((((aDataVsArea_NIU3ESRErrLo[i] + aDataVsArea_NIU3ESRErrHi[i])/2)/aDataVsArea_NIU3ESR[i])**2 + (aSimVsArea_3ESRErr_NIU[i]/aSimVsArea_3ESR_NIU[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsArea_3ESR_NIU)):
        aSimVsArea_3ESR_NIU[i] = aSimVsArea_3ESR_NIU[i]*Norm
        aSimVsArea_3ESRErr_NIU[i] = aSimVsArea_3ESRErr_NIU[i]*Norm

### Creating Graphs ###
if Samples == "Tyvek":
    grSimulation = r.TGraphErrors(len(aTyvekAreas),aTyvekAreas,aSimVsArea_Tyvek,aAreas3p8_Err,aSimVsArea_TyvekErr)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphAsymmErrors(len(aTyvekAreas), aAreaSizes_Tyvek, aDataVsArea_Tyvek, aAreas3p8_Err, aAreas3p8_Err, aDataVsArea_TyvekErrLo, aDataVsArea_TyvekErrHi)
elif Samples == "ESR_3p8":
    grSimulation = r.TGraphErrors(len(aESR3p8Areas),aESR3p8Areas,aSimVsArea_3p8ESR,aAreas3p8_Err,aSimVsArea_3p8ESRErr)
    grData = r.TGraphAsymmErrors(len(aAreaSizes_3p8ESR),aAreaSizes_3p8ESR,aDataVsArea_3p8ESR, aAreas3p8_Err, aAreas3p8_Err, aDataVsArea_3p8ESRErrLo, aDataVsArea_3p8ESRErrHi)
    grMax = r.TMath.MaxElement(grData.GetN(),grData.GetY())

elif Samples == "EJ200_3ESR":
    grSimulation = r.TGraphErrors(len(aESR3Areas_EJ200),aESR3Areas_EJ200,aSimVsArea_3ESR,aAreas3_Err,aSimVsArea_3ESRErr)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphAsymmErrors(len(aAreaSizes_EJ3ESR),aAreaSizes_EJ3ESR,aDataVsArea_EJ3ESR, aAreas3_Err, aAreas3_Err, aDataVsArea_EJ3ESRErrLo, aDataVsArea_EJ3ESRErrHi)
elif Samples == "NIU_3ESR":
    grSimulation = r.TGraphErrors(len(aESR3Areas_NIU),aESR3Areas_NIU,aSimVsArea_3ESR_NIU,aAreas3_Err,aSimVsArea_3ESRErr_NIU)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphAsymmErrors(len(aAreaSizes_NIU3ESR),aAreaSizes_NIU3ESR,aDataVsArea_NIU3ESR, aAreas3_Err, aAreas3_Err, aDataVsArea_NIU3ESRErrLo, aDataVsArea_NIU3ESRErrHi)



grSimulation.SetTitle("")
grSimulation.SetMarkerColor(r.kRed)
grSimulation.SetLineColor(r.kRed)
grSimulation.SetMarkerSize(2.5)
grSimulation.SetMarkerStyle(32)
grSimulation.GetXaxis().SetTitle("Tile Area (cm^{2})")
grSimulation.GetYaxis().SetTitle("MPV (PE)")
grSimulation.GetYaxis().SetRangeUser(0, 1.7*grMax)
grSimulation.GetXaxis().SetLabelSize(0)
grSimulation.GetYaxis().SetTitleSize(.2*3/7)
grSimulation.GetYaxis().SetLabelSize(.2*3/7)

grData.SetMarkerColor(r.kBlack)
grData.SetMarkerSize(2.5)
grData.SetMarkerStyle(8)

grSimulation_shifted = grSimulation.Clone("grSimulation_shifted")
grData_shifted       = grData.Clone("grData_shifted")

### Shifting the x-positions of the graphs so that they are side-by-side ###
shift = (grSimulation_shifted.GetX()[grSimulation_shifted.GetN() - 1] - grSimulation_shifted.GetX()[0])/60.

for i in range(0,grSimulation_shifted.GetN()):
    grSimulation_shifted.SetPoint(i, grSimulation.GetX()[i] + shift, grSimulation.GetY()[i])
    grData_shifted.SetPoint(i, grData.GetX()[i] - shift, grData.GetY()[i])


grSimulation_shifted.GetYaxis().SetRangeUser(0, 1.7*grMax)
grSimulation_shifted.SetMarkerColor(r.kRed)
grSimulation_shifted.SetLineColor(r.kRed)
grSimulation_shifted.SetMarkerSize(2.5)
grSimulation_shifted.SetMarkerStyle(32)
grSimulation_shifted.GetXaxis().SetTitle("Tile Area (cm^{2})")
grSimulation_shifted.GetYaxis().SetTitle("MPV (PE)")
grSimulation_shifted.GetYaxis().SetRangeUser(0, 1.7*grMax)
grSimulation_shifted.GetXaxis().SetLabelSize(0)
grSimulation_shifted.GetYaxis().SetTitleSize(.15*3/7)
grSimulation_shifted.GetYaxis().SetLabelSize(.15*3/7)
grSimulation_shifted.GetYaxis().SetTitleOffset(0.8)

simFit = r.TF1("simFit","[0]*(x/9.)^[1]",0,30)
simFit.SetLineColor(r.kBlack)
grData_shifted.Fit("simFit")
#grSimulation_shifted.Fit("simFit")

#c = r.TCanvas("c","c")
c = r.TCanvas("c","c",1000,1000)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetBorderSize(2)
c.SetFrameBorderMode(0)

oben = r.TPad('oben','oben',0,0.3 ,1.0,1.0)
unten = r.TPad('unten','unten',0,0.0,1.0,0.3)
canvas_margin(c,oben,unten)

oben.SetFillStyle(4000)
oben.SetFrameFillStyle(1000)
oben.SetFrameFillColor(0)
unten.SetFillStyle(4000)
unten.SetFrameFillStyle(1000)
unten.SetFrameFillColor(0)
oben.Draw()
unten.Draw()

CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()

oben.cd()

grSimulation_shifted.Draw("AP")
grData_shifted.Draw("P same")

legend = r.TLegend(0.66,0.61,0.97,0.93)
legend.SetFillStyle(0)
legend.SetBorderSize(1)
legend.SetTextSize(0.065)
legend.SetTextFont(42)

legend.AddEntry(grSimulation, "Simulation", "PE")
legend.AddEntry(grData, "Data", "PE")
legend.AddEntry(simFit, "Data Fit", "L")
#legend.AddEntry(simFit, "Simulation Fit", "L")

legend.Draw("same")

fitInfo = r.TLatex()
par0 = simFit.GetParameter(0)
par1 = simFit.GetParameter(1)
chi2 = simFit.GetChisquare()
ndf  = simFit.GetNDF()

print "par0: ", par0
print "par1: ", par1
print "chi2/ndf: ", chi2/ndf

fitInfo.SetTextAlign(12)
fitInfo.SetTextSize(0.06)
#fitInfo.DrawLatexNDC(0.32,0.86,"MPV = (%.2f)Area^{%.2f}"%(par0,par1))

### Ratio plot ###
unten.cd()

Ratio, RatioErrLo, RatioErrHi, Zero = getRatio(grData, grSimulation)
aRatio      = array.array('d', Ratio)
aRatioErrLo = array.array('d', RatioErrLo)
aRatioErrHi = array.array('d', RatioErrHi)
aZero       = array.array('d', Zero)

grRatio = r.TGraphAsymmErrors(len(Ratio),grData.GetX(),aRatio,aZero, aZero ,aRatioErrLo, aRatioErrHi)
MaxRatio = r.TMath.MaxElement(grRatio.GetN(),grRatio.GetY())
MinRatio = max(2. - MaxRatio, 0.)

grRatio.SetTitle("")
grRatio.SetMarkerColor(r.kBlack)
grRatio.SetMarkerSize(2.5)
grRatio.SetMarkerStyle(8)
grRatio.GetXaxis().SetTitle("Tile Area (cm^{2})")
grRatio.GetXaxis().SetTitleSize(.15)
grRatio.GetXaxis().SetLabelSize(.15)
grRatio.GetYaxis().SetTitle("#frac{Data}{Sim.}")
grRatio.GetYaxis().SetTitleSize(.15)
grRatio.GetYaxis().SetTitleOffset(0.4)
grRatio.GetYaxis().CenterTitle()
grRatio.GetYaxis().SetLabelSize(.15)
grRatio.GetYaxis().SetNdivisions(5, r.kTRUE)
grRatio.GetYaxis().SetRangeUser(MinRatio - 0.2, MaxRatio + 0.2)

grRatio.Draw("AP")

Ratio_allErr = getMCratioError(grSimulation)

Ratio_allErr.SetMarkerColor(r.kRed)
Ratio_allErr.SetMarkerSize(0)
Ratio_allErr.SetFillStyle(3013)
Ratio_allErr.SetFillColor(r.kRed)
Ratio_allErr.SetLineColor(0)
#Ratio_allErr.Draw("E2same")


c.SaveAs("Data_vs_Simulation_Area_" + Samples +".pdf")
