import ROOT as r
import sys
import datetime
import subprocess
import os
import copy
import sets
import collections
import math
import tdrstyle
import array
import numpy as np

### Returns the data/sim ratio and the data error/sim ratio ###
def getRatio(dataGraph, simGraph):

    ratio    = []
    ratioErr = []
    zero     = []
    for i in range(0,dataGraph.GetN()):
	ratio.append(dataGraph.GetY()[i]/simGraph.GetY()[i])
	ratioErr.append(dataGraph.GetEY()[i]/simGraph.GetY()[i])
	zero.append(0.0)


    return ratio, ratioErr, zero

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
SimVsArea_Tyvek     = [78.05, 57.14, 44.1]
SimVsArea_TyvekErr  = [11.87, 8.11, 6.75]

SimVsArea_3p8ESR    = [90.51, 65.95, 51.88]
SimVsArea_3p8ESRErr = [13.32, 8.73, 7.61]

SimVsArea_3ESR     = [97.17, 75.95, 67.34, 41.44]
SimVsArea_3ESRErr  = [21.99, 13.81, 10.93, 6.86]

SimVsArea_3ESR_NIU     = [67.34, 65.36, 61.91, 60.4]
SimVsArea_3ESRErr_NIU  = [10.93, 10.64, 10.05, 9.84]

SimVsArea_3ESR_all     = [97.17, 75.95, 67.34, 65.36, 61.91, 60.4, 41.44]
SimVsArea_3ESRErr_all  = [21.99, 13.81, 10.93, 10.64, 10.05, 9.84, 6.86]


aSimVsArea_Tyvek     = array.array('d', SimVsArea_Tyvek)
aSimVsArea_TyvekErr  = array.array('d', SimVsArea_TyvekErr)
aSimVsArea_3p8ESR    = array.array('d', SimVsArea_3p8ESR)
aSimVsArea_3p8ESRErr = array.array('d', SimVsArea_3p8ESRErr)
aSimVsArea_3ESR      = array.array('d', SimVsArea_3ESR)
aSimVsArea_3ESRErr   = array.array('d', SimVsArea_3ESRErr)
aSimVsArea_3ESR_NIU      = array.array('d', SimVsArea_3ESR_NIU)
aSimVsArea_3ESRErr_NIU   = array.array('d', SimVsArea_3ESRErr_NIU)

### Data Results ###
Error = 0.0176
AreaSizes_Tyvek   = [9, 16, 25]
AreaSizes_3p8ESR  = [9, 16, 25]
AreaSizes_EJ3ESR  = [2.3*2.3, 9, 3.4*3.4, 5.5*5.5]
AreaSizes_NIU3ESR = [3.4*3.4, 3.5*3.5, 3.7*3.7, 3.8*3.8]

DataVsArea_Tyvek   = [7.69, 5.65, 4.38]
DataVsArea_3p8ESR  = [25.53, 15.39, 7.47]
DataVsArea_EJ3ESR  = [39.55, 32.23, 25.97, 14.71]
DataVsArea_NIU3ESR = [19.07, 21.17, 17.32, 17.71]

DataVsArea_TyvekErr     = Error*np.array(DataVsArea_Tyvek)
DataVsArea_3p8ESRErr    = Error*np.array(DataVsArea_3p8ESR)
DataVsArea_EJ3ESRErr    = Error*np.array(DataVsArea_EJ3ESR)
DataVsArea_NIU3ESRErr   = Error*np.array(DataVsArea_NIU3ESR)

aAreaSizes_Tyvek   = array.array('d', AreaSizes_Tyvek)
aAreaSizes_3p8ESR  = array.array('d', AreaSizes_3p8ESR)
aAreaSizes_EJ3ESR  = array.array('d', AreaSizes_EJ3ESR)
aAreaSizes_NIU3ESR = array.array('d', AreaSizes_NIU3ESR)

aDataVsArea_Tyvek   = array.array('d', DataVsArea_Tyvek)
aDataVsArea_3p8ESR  = array.array('d', DataVsArea_3p8ESR)
aDataVsArea_EJ3ESR  = array.array('d', DataVsArea_EJ3ESR)
aDataVsArea_NIU3ESR = array.array('d', DataVsArea_NIU3ESR)

aDataVsArea_TyvekErr  = array.array('d', DataVsArea_TyvekErr)
aDataVsArea_3p8ESRErr  = array.array('d', DataVsArea_3p8ESRErr)
aDataVsArea_EJ3ESRErr  = array.array('d', DataVsArea_EJ3ESRErr)
aDataVsArea_NIU3ESRErr = array.array('d', DataVsArea_NIU3ESRErr)


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
        normGraph.SetBinContent(i, aDataVsArea_Tyvek[i]/aSimVsArea_Tyvek[i])

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
        normGraph.SetBinContent(i, aDataVsArea_3p8ESR[i]/aSimVsArea_3p8ESR[i])

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
	normGraph.SetBinContent(i, aDataVsArea_EJ3ESR[i]/aSimVsArea_3ESR[i])

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
        normGraph.SetBinContent(i, aDataVsArea_NIU3ESR[i]/aSimVsArea_3ESR_NIU[i])

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
    grData = r.TGraphErrors(len(aTyvekAreas), aAreaSizes_Tyvek, aDataVsArea_Tyvek, aAreas3p8_Err, aDataVsArea_TyvekErr)
elif Samples == "ESR_3p8":
    grSimulation = r.TGraphErrors(len(aESR3p8Areas),aESR3p8Areas,aSimVsArea_3p8ESR,aAreas3p8_Err,aSimVsArea_3p8ESRErr)
    grData = r.TGraphErrors(len(aAreaSizes_3p8ESR),aAreaSizes_3p8ESR,aDataVsArea_3p8ESR, aAreas3p8_Err, aDataVsArea_3p8ESRErr)
    grMax = r.TMath.MaxElement(grData.GetN(),grData.GetY())

elif Samples == "EJ200_3ESR":
    grSimulation = r.TGraphErrors(len(aESR3Areas_EJ200),aESR3Areas_EJ200,aSimVsArea_3ESR,aAreas3_Err,aSimVsArea_3ESRErr)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphErrors(len(aAreaSizes_EJ3ESR),aAreaSizes_EJ3ESR,aDataVsArea_EJ3ESR, aAreas3_Err, aDataVsArea_EJ3ESRErr)
elif Samples == "NIU_3ESR":
    grSimulation = r.TGraphErrors(len(aESR3Areas_NIU),aESR3Areas_NIU,aSimVsArea_3ESR_NIU,aAreas3_Err,aSimVsArea_3ESRErr_NIU)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphErrors(len(aAreaSizes_NIU3ESR),aAreaSizes_NIU3ESR,aDataVsArea_NIU3ESR, aAreas3_Err, aDataVsArea_NIU3ESRErr)



grSimulation.SetTitle("")
grSimulation.SetMarkerColor(r.kRed)
grSimulation.SetLineColor(r.kRed)
grSimulation.SetMarkerSize(2.5)
grSimulation.SetMarkerStyle(32)
grSimulation.GetXaxis().SetTitle("Tile Area (cm^{2})")
grSimulation.GetYaxis().SetTitle("MPV (PE)")
grSimulation.GetYaxis().SetRangeUser(0, 1.5*grMax)
grSimulation.GetXaxis().SetLabelSize(0)
grSimulation.GetYaxis().SetTitleSize(.12*3/7)
grSimulation.GetYaxis().SetLabelSize(.12*3/7)

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


grSimulation_shifted.GetYaxis().SetRangeUser(0, 1.5*grMax)
grSimulation_shifted.SetMarkerColor(r.kRed)
grSimulation_shifted.SetLineColor(r.kRed)
grSimulation_shifted.SetMarkerSize(2.5)
grSimulation_shifted.SetMarkerStyle(32)
grSimulation_shifted.GetXaxis().SetTitle("Tile Area (cm^{2})")
grSimulation_shifted.GetYaxis().SetTitle("MPV (PE)")
grSimulation_shifted.GetYaxis().SetRangeUser(0, 1.5*grMax)
grSimulation_shifted.GetXaxis().SetLabelSize(0)
grSimulation_shifted.GetYaxis().SetTitleSize(.12*3/7)
grSimulation_shifted.GetYaxis().SetLabelSize(.12*3/7)

simFit = r.TF1("simFit","[0]*x^[1]",0,30)
grSimulation_shifted.Fit("simFit")

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
oben.cd()

grSimulation_shifted.Draw("AP")
grData_shifted.Draw("P same")

legend = r.TLegend(0.66,0.76,0.97,0.93)
legend.SetFillStyle(0)
legend.SetBorderSize(1)
legend.SetTextSize(0.065)
legend.SetTextFont(42)

legend.AddEntry(grSimulation, "Simulation", "PE")
legend.AddEntry(grData, "Data", "PE")

legend.Draw("same")

fitInfo = r.TLatex()
par0 = simFit.GetParameter(0)
par1 = simFit.GetParameter(1)

print "par0: ", par0
print "par1: ", par1

fitInfo.SetTextAlign(12)
fitInfo.SetTextSize(0.06)
fitInfo.DrawLatexNDC(0.25,0.88,"MPV = (%.2f)Area^{%.2f}"%(par0,par1))

### Ratio plot ###
unten.cd()

Ratio, RatioErr, Zero = getRatio(grData, grSimulation)
aRatio    = array.array('d', Ratio)
aRatioErr = array.array('d', RatioErr)
aZero     = array.array('d', Zero)

grRatio = r.TGraphErrors(len(Ratio),grData.GetX(),aRatio,aZero,aRatioErr)
MaxRatio = r.TMath.MaxElement(grRatio.GetN(),grRatio.GetY())
MinRatio = max(2. - MaxRatio, 0.)

grRatio.SetTitle("")
grRatio.SetMarkerColor(r.kBlack)
grRatio.SetMarkerSize(2.5)
grRatio.SetMarkerStyle(8)
grRatio.GetXaxis().SetTitle("Tile Area (cm^{2})")
grRatio.GetXaxis().SetTitleSize(.12)
grRatio.GetXaxis().SetLabelSize(.12)
grRatio.GetYaxis().SetTitle("#frac{Data}{Sim.}")
grRatio.GetYaxis().SetTitleSize(.12)
grRatio.GetYaxis().SetTitleOffset(0.45)
grRatio.GetYaxis().CenterTitle()
grRatio.GetYaxis().SetLabelSize(.12)
grRatio.GetYaxis().SetNdivisions(5, r.kTRUE)
grRatio.GetYaxis().SetRangeUser(MinRatio - 0.2, MaxRatio + 0.2)

grRatio.Draw("AP")

Ratio_allErr = getMCratioError(grSimulation)

Ratio_allErr.SetMarkerColor(r.kRed)
Ratio_allErr.SetMarkerSize(0)
Ratio_allErr.SetFillStyle(3013)
Ratio_allErr.SetFillColor(r.kRed)
Ratio_allErr.SetLineColor(0)
Ratio_allErr.Draw("E2same")


c.SaveAs("Data_vs_Simulation_Area_" + Samples +".pdf")
