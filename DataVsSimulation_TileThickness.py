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

    ratio    = []
    ratioErr = []
    zero     = []
    doubleMeasurements = 0
    if dataGraph.GetN() == simGraph.GetN():
	for i in range(0,dataGraph.GetN()):
            ratio.append(dataGraph.GetY()[i]/simGraph.GetY()[i])
            ratioErr.append(dataGraph.GetEY()[i]/simGraph.GetY()[i])
            zero.append(0.0)
    else:
        for i in range(0,dataGraph.GetN()):
	    if dataGraph.GetX()[i] == simGraph.GetX()[i]:
                ratio.append(dataGraph.GetY()[i]/simGraph.GetY()[i])
                ratioErr.append(dataGraph.GetEY()[i]/simGraph.GetY()[i])
                zero.append(0.0)
	    else:
		if dataGraph.GetX()[i] == dataGraph.GetX()[i-1]:
		    doubleMeasurements = doubleMeasurements + 1
		ratio.append(dataGraph.GetY()[i]/simGraph.GetY()[i-doubleMeasurements])
                ratioErr.append(dataGraph.GetEY()[i]/simGraph.GetY()[i-doubleMeasurements])
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
TileWidths  = [3.8, 7.6, 11.4]

TileWidths_Err   = [0, 0, 0]

aTileWidths     = array.array('d', TileWidths)
aTileWidths_Err = array.array('d', TileWidths_Err)

### Simulation Results ###
SimVsWidth_Tyvek3x3     = [78.05, 103, 118]
SimVsWidth_Tyvek3x3_Err = [11.87, 11.26, 11.46]

SimVsWidth_ESR3x3     = [90.51, 132.4, 156.4]
SimVsWidth_ESR3x3_Err = [13.32, 12.39, 13.16]

SimVsWidth_Tyvek4x4     = [57.14, 67.98, 75.09]
SimVsWidth_Tyvek4x4_Err = [8.11, 8.23, 8.82]

SimVsWidth_ESR4x4     = [65.95, 88.17, 100.3]
SimVsWidth_ESR4x4_Err = [8.73, 9.68, 10.21]

SimVsWidth_Tyvek5x5     = [44.1, 48.56, 52.04]
SimVsWidth_Tyvek5x5_Err = [6.75, 6.99, 7.55]

SimVsWidth_ESR5x5     = [51.88, 64.48, 70.24]
SimVsWidth_ESR5x5_Err = [7.61, 8.54, 8.974]


aSimVsWidth_Tyvek3x3     = array.array('d', SimVsWidth_Tyvek3x3)
aSimVsWidth_Tyvek3x3_Err = array.array('d', SimVsWidth_Tyvek3x3_Err)
aSimVsWidth_ESR3x3       = array.array('d', SimVsWidth_ESR3x3)
aSimVsWidth_ESR3x3_Err   = array.array('d', SimVsWidth_ESR3x3_Err)
aSimVsWidth_Tyvek4x4     = array.array('d', SimVsWidth_Tyvek4x4)
aSimVsWidth_Tyvek4x4_Err = array.array('d', SimVsWidth_Tyvek4x4_Err)
aSimVsWidth_ESR4x4       = array.array('d', SimVsWidth_ESR4x4)
aSimVsWidth_ESR4x4_Err   = array.array('d', SimVsWidth_ESR4x4_Err)
aSimVsWidth_Tyvek5x5     = array.array('d', SimVsWidth_Tyvek5x5)
aSimVsWidth_Tyvek5x5_Err = array.array('d', SimVsWidth_Tyvek5x5_Err)
aSimVsWidth_ESR5x5       = array.array('d', SimVsWidth_ESR5x5)
aSimVsWidth_ESR5x5_Err   = array.array('d', SimVsWidth_ESR5x5_Err)

### Data Results ###
Error = 0.064344
TileWidths_ESR4x4     = [3.8, 7.6, 7.6, 11.4]
TileWidths_ESR4x4_all = [3.8, 7.6, 7.6, 7.6, 11.4, 11.4]
TileWidths_ESR5x5     = [3.8, 7.6, 7.6, 11.4, 11.4]

DataVsWidth_Tyvek3x3     = [7.69, 9.74, 10.78]
DataVsWidth_ESR3x3       = [25.53, 29.11, 44.3]
DataVsWidth_Tyvek4x4     = [5.65, 8.12, 8.04]
DataVsWidth_ESR4x4       = [15.39, 20.67, 22., 32.37]
DataVsWidth_ESR4x4_all   = [15.39, 13.50, 20.67, 22., 15.43, 32.37]
DataVsWidth_Tyvek5x5     = [4.38, 5.57, 5.37]
DataVsWidth_ESR5x5       = [7.47, 14.56, 15.01, 16.95, 16.82]

DataVsWidth_Tyvek3x3Err  = Error*np.array(DataVsWidth_Tyvek3x3)
DataVsWidth_ESR3x3Err    = Error*np.array(DataVsWidth_ESR3x3)
DataVsWidth_Tyvek4x4Err  = Error*np.array(DataVsWidth_Tyvek4x4)
DataVsWidth_ESR4x4Err    = Error*np.array(DataVsWidth_ESR4x4)
DataVsWidth_Tyvek5x5Err  = Error*np.array(DataVsWidth_Tyvek5x5)
DataVsWidth_ESR5x5Err    = Error*np.array(DataVsWidth_ESR5x5)

aTileWidths_ESR4x4  = array.array('d', TileWidths_ESR4x4)
aTileWidths_ESR5x5  = array.array('d', TileWidths_ESR5x5)

aDataVsWidth_Tyvek3x3 = array.array('d', DataVsWidth_Tyvek3x3)
aDataVsWidth_ESR3x3   = array.array('d', DataVsWidth_ESR3x3)
aDataVsWidth_Tyvek4x4 = array.array('d', DataVsWidth_Tyvek4x4)
aDataVsWidth_ESR4x4   = array.array('d', DataVsWidth_ESR4x4)
aDataVsWidth_Tyvek5x5 = array.array('d', DataVsWidth_Tyvek5x5)
aDataVsWidth_ESR5x5   = array.array('d', DataVsWidth_ESR5x5)

aDataVsWidth_Tyvek3x3Err = array.array('d', DataVsWidth_Tyvek3x3Err)
aDataVsWidth_ESR3x3Err   = array.array('d', DataVsWidth_ESR3x3Err)
aDataVsWidth_Tyvek4x4Err = array.array('d', DataVsWidth_Tyvek4x4Err)
aDataVsWidth_ESR4x4Err   = array.array('d', DataVsWidth_ESR4x4Err)
aDataVsWidth_Tyvek5x5Err = array.array('d', DataVsWidth_Tyvek5x5Err)
aDataVsWidth_ESR5x5Err   = array.array('d', DataVsWidth_ESR5x5Err)



############################################
if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print "Please use Tyvek3x3, ESR3x3, Tyvek4x4, ESR4x4, Tyvek5x5, or ESR5x5 as an argument"
    exit(0)
elif len(sys.argv) == 1:
    print "Please use Tyvek3x3, ESR3x3, Tyvek4x4, ESR4x4, Tyvek5x5, or ESR5x5 as an argument"
    exit(0)


Samples = sys.argv[1]

if Samples != "Tyvek3x3" and Samples != "ESR3x3" and Samples != "Tyvek4x4" and Samples != "ESR4x4" and Samples != "Tyvek5x5" and Samples != "ESR5x5":
    print "Please use Tyvek3x3, ESR3x3, Tyvek4x4, ESR4x4, Tyvek5x5, or ESR5x5 as an argument"
    exit(0)


### Normalizing Simulation ###
if Samples == "ESR3x3":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsWidth_ESR3x3), 0, 1)

    for i in range(0, len(aSimVsWidth_ESR3x3)):
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR3x3[i]/aSimVsWidth_ESR3x3[i])
	Error = (aDataVsWidth_ESR3x3[i]/aSimVsWidth_ESR3x3[i])*math.sqrt((aDataVsWidth_ESR3x3Err[i]/aDataVsWidth_ESR3x3[i])**2 + (aSimVsWidth_ESR3x3_Err[i]/aSimVsWidth_ESR3x3[i])**2)
	normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsWidth_ESR3x3)):
	aSimVsWidth_ESR3x3[i] = aSimVsWidth_ESR3x3[i]*Norm
    	aSimVsWidth_ESR3x3_Err[i] = aSimVsWidth_ESR3x3_Err[i]*Norm
elif Samples == "Tyvek3x3":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsWidth_Tyvek3x3), 0, 1)

    for i in range(0, len(aSimVsWidth_Tyvek3x3)):
        normGraph.SetBinContent(i+1, aDataVsWidth_Tyvek3x3[i]/aSimVsWidth_Tyvek3x3[i])
        Error = (aDataVsWidth_Tyvek3x3[i]/aSimVsWidth_Tyvek3x3[i])*math.sqrt((aDataVsWidth_Tyvek3x3Err[i]/aDataVsWidth_Tyvek3x3[i])**2 + (aSimVsWidth_Tyvek3x3_Err[i]/aSimVsWidth_Tyvek3x3[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsWidth_Tyvek3x3)):
        aSimVsWidth_Tyvek3x3[i] = aSimVsWidth_Tyvek3x3[i]*Norm
        aSimVsWidth_Tyvek3x3_Err[i] = aSimVsWidth_Tyvek3x3_Err[i]*Norm
elif Samples == "ESR4x4":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsWidth_ESR4x4), 0, 1)

    for i in range(0, len(aDataVsWidth_ESR4x4)):
      if (i+1 > len(aTileWidths)):
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR4x4[i]/aSimVsWidth_ESR4x4[i-1])
        Error = (aDataVsWidth_ESR4x4[i]/aSimVsWidth_ESR4x4[i-1])*math.sqrt((aDataVsWidth_ESR4x4Err[i]/aDataVsWidth_ESR4x4[i])**2 + (aSimVsWidth_ESR4x4_Err[i-1]/aSimVsWidth_ESR4x4[i-1])**2)
        normGraph.SetBinError(i+1, Error)
      elif aTileWidths[i] == aTileWidths_ESR4x4[i]:
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR4x4[i]/aSimVsWidth_ESR4x4[i])
        Error = (aDataVsWidth_ESR4x4[i]/aSimVsWidth_ESR4x4[i])*math.sqrt((aDataVsWidth_ESR4x4Err[i]/aDataVsWidth_ESR4x4[i])**2 + (aSimVsWidth_ESR4x4_Err[i]/aSimVsWidth_ESR4x4[i])**2)
        normGraph.SetBinError(i+1, Error)
      else:
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR4x4[i]/aSimVsWidth_ESR4x4[i-1])
        Error = (aDataVsWidth_ESR4x4[i]/aSimVsWidth_ESR4x4[i-1])*math.sqrt((aDataVsWidth_ESR4x4Err[i]/aDataVsWidth_ESR4x4[i])**2 + (aSimVsWidth_ESR4x4_Err[i-1]/aSimVsWidth_ESR4x4[i-1])**2)
        normGraph.SetBinError(i+1, Error)


    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsWidth_ESR4x4)):
        aSimVsWidth_ESR4x4[i] = aSimVsWidth_ESR4x4[i]*Norm
        aSimVsWidth_ESR4x4_Err[i] = aSimVsWidth_ESR4x4_Err[i]*Norm
elif Samples == "Tyvek4x4":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsWidth_Tyvek4x4), 0, 1)

    for i in range(0, len(aSimVsWidth_Tyvek4x4)):
        normGraph.SetBinContent(i+1, aDataVsWidth_Tyvek4x4[i]/aSimVsWidth_Tyvek4x4[i])
        Error = (aDataVsWidth_Tyvek4x4[i]/aSimVsWidth_Tyvek4x4[i])*math.sqrt((aDataVsWidth_Tyvek4x4Err[i]/aDataVsWidth_Tyvek4x4[i])**2 + (aSimVsWidth_Tyvek4x4_Err[i]/aSimVsWidth_Tyvek4x4[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsWidth_Tyvek4x4)):
        aSimVsWidth_Tyvek4x4[i] = aSimVsWidth_Tyvek4x4[i]*Norm
        aSimVsWidth_Tyvek4x4_Err[i] = aSimVsWidth_Tyvek4x4_Err[i]*Norm
elif Samples == "ESR5x5":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsWidth_ESR5x5), 0, 1)

    for i in range(0, len(aDataVsWidth_ESR5x5)):
      if (i ==  len(aTileWidths)):
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i-1])
        Error = (aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i-1])*math.sqrt((aDataVsWidth_ESR5x5Err[i]/aDataVsWidth_ESR5x5[i])**2 + (aSimVsWidth_ESR5x5_Err[i-1]/aSimVsWidth_ESR5x5[i-1])**2)
        normGraph.SetBinError(i+1, Error)
      elif (i-1 == len(aTileWidths)):
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i-2])
        Error = (aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i-2])*math.sqrt((aDataVsWidth_ESR5x5Err[i]/aDataVsWidth_ESR5x5[i])**2 + (aSimVsWidth_ESR5x5_Err[i-2]/aSimVsWidth_ESR5x5[i-2])**2)
        normGraph.SetBinError(i+1, Error)
      elif aTileWidths[i] == aTileWidths_ESR5x5[i]:
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i])
        Error = (aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i])*math.sqrt((aDataVsWidth_ESR5x5Err[i]/aDataVsWidth_ESR5x5[i])**2 + (aSimVsWidth_ESR5x5_Err[i]/aSimVsWidth_ESR5x5[i])**2)
        normGraph.SetBinError(i+1, Error)
      else:
        normGraph.SetBinContent(i+1, aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i-1])
        Error = (aDataVsWidth_ESR5x5[i]/aSimVsWidth_ESR5x5[i-1])*math.sqrt((aDataVsWidth_ESR5x5Err[i]/aDataVsWidth_ESR5x5[i])**2 + (aSimVsWidth_ESR5x5_Err[i-1]/aSimVsWidth_ESR5x5[i-1])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsWidth_ESR5x5)):
        aSimVsWidth_ESR5x5[i] = aSimVsWidth_ESR5x5[i]*Norm
        aSimVsWidth_ESR5x5_Err[i] = aSimVsWidth_ESR5x5_Err[i]*Norm
elif Samples == "Tyvek5x5":
    normGraph = r.TH1F("normGraph","normGraph",len(aDataVsWidth_Tyvek5x5), 0, 1)

    for i in range(0, len(aSimVsWidth_Tyvek5x5)):
        normGraph.SetBinContent(i+1, aDataVsWidth_Tyvek5x5[i]/aSimVsWidth_Tyvek5x5[i])
        Error = (aDataVsWidth_Tyvek5x5[i]/aSimVsWidth_Tyvek5x5[i])*math.sqrt((aDataVsWidth_Tyvek5x5Err[i]/aDataVsWidth_Tyvek5x5[i])**2 + (aSimVsWidth_Tyvek5x5_Err[i]/aSimVsWidth_Tyvek5x5[i])**2)
        normGraph.SetBinError(i+1, Error)

    fit = r.TF1("fit","[0]")
    normGraph.Fit("fit")

    Norm = fit.GetParameter(0)
    print "Norm: ", Norm
    for i in range(0, len(aSimVsWidth_Tyvek5x5)):
        aSimVsWidth_Tyvek5x5[i] = aSimVsWidth_Tyvek5x5[i]*Norm
        aSimVsWidth_Tyvek5x5_Err[i] = aSimVsWidth_Tyvek5x5_Err[i]*Norm

### Plotting ###
if Samples == "Tyvek3x3":
    grSimulation = r.TGraphErrors(len(aTileWidths),aTileWidths,aSimVsWidth_Tyvek3x3,aTileWidths_Err,aSimVsWidth_Tyvek3x3_Err)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphErrors(len(aTileWidths), aTileWidths, aDataVsWidth_Tyvek3x3, aTileWidths_Err, aDataVsWidth_Tyvek3x3Err)
elif Samples == "ESR3x3":
    grSimulation = r.TGraphErrors(len(aTileWidths),aTileWidths,aSimVsWidth_ESR3x3,aTileWidths_Err,aSimVsWidth_ESR3x3_Err)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphErrors(len(aTileWidths), aTileWidths, aDataVsWidth_ESR3x3,  aTileWidths_Err, aDataVsWidth_ESR3x3Err)
elif Samples == "Tyvek4x4":
    grSimulation = r.TGraphErrors(len(aTileWidths),aTileWidths,aSimVsWidth_Tyvek4x4,aTileWidths_Err,aSimVsWidth_Tyvek4x4_Err)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphErrors(len(aTileWidths), aTileWidths, aDataVsWidth_Tyvek4x4, aTileWidths_Err, aDataVsWidth_Tyvek4x4Err)
elif Samples == "ESR4x4":
    grSimulation = r.TGraphErrors(len(aTileWidths),aTileWidths,aSimVsWidth_ESR4x4,aTileWidths_Err,aSimVsWidth_ESR4x4_Err)
    grData = r.TGraphErrors(len(aTileWidths_ESR4x4), aTileWidths_ESR4x4, aDataVsWidth_ESR4x4, aTileWidths_Err, aDataVsWidth_ESR4x4Err)
    grMax = r.TMath.MaxElement(grData.GetN(),grData.GetY())
elif Samples == "Tyvek5x5":
    grSimulation = r.TGraphErrors(len(aTileWidths),aTileWidths,aSimVsWidth_Tyvek5x5,aTileWidths_Err,aSimVsWidth_Tyvek5x5_Err)
    grMax = r.TMath.MaxElement(grSimulation.GetN(),grSimulation.GetY())
    grData = r.TGraphErrors(len(aTileWidths), aTileWidths, aDataVsWidth_Tyvek5x5, aTileWidths_Err, aDataVsWidth_Tyvek5x5Err)
elif Samples == "ESR5x5":
    grSimulation = r.TGraphErrors(len(aTileWidths),aTileWidths,aSimVsWidth_ESR5x5,aTileWidths_Err,aSimVsWidth_ESR5x5_Err)
    grData = r.TGraphErrors(len(aTileWidths_ESR5x5), aTileWidths_ESR5x5, aDataVsWidth_ESR5x5, aTileWidths_Err, aDataVsWidth_ESR5x5Err)
    grMax = r.TMath.MaxElement(grData.GetN(),grData.GetY())



grSimulation.SetTitle("")
grSimulation.SetMarkerColor(r.kRed)
grSimulation.SetLineColor(r.kRed)
grSimulation.SetMarkerSize(2.5)
grSimulation.SetMarkerStyle(32)
grSimulation.GetXaxis().SetTitle("Tile Thickness (cm)")
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
grSimulation_shifted.GetXaxis().SetTitle("Tile Thickness (cm)")
grSimulation_shifted.GetYaxis().SetTitle("MPV (PE)")
grSimulation_shifted.GetYaxis().SetRangeUser(0, 1.5*grMax)
grSimulation_shifted.GetXaxis().SetLabelSize(0)
grSimulation_shifted.GetYaxis().SetTitleSize(.15*3/7)
grSimulation_shifted.GetYaxis().SetLabelSize(.15*3/7)
grSimulation_shifted.GetYaxis().SetTitleOffset(0.8)

simFit = r.TF1("simFit","[0]*x^[1]",0,30)
grSimulation_shifted.Fit("simFit")

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

legend = r.TLegend(0.66,0.68,0.97,0.93)
legend.SetFillStyle(0)
legend.SetBorderSize(1)
legend.SetTextSize(0.065)
legend.SetTextFont(42)

legend.AddEntry(grSimulation, "Simulation", "PE")
legend.AddEntry(grData, "Data", "PE")
legend.AddEntry(simFit, "Fit", "L")

legend.Draw("same")

fitInfo = r.TLatex()
par0 = simFit.GetParameter(0)
par1 = simFit.GetParameter(1)

print "par0: ", par0
print "par1: ", par1

fitInfo.SetTextAlign(12)
fitInfo.SetTextSize(0.06)
fitInfo.DrawLatexNDC(0.32,0.86,"MPV = (%.2f)Area^{%.2f}"%(par0,par1))


### Ratio plot ###
unten.cd()

Ratio, RatioErr, Zero = getRatio(grData, grSimulation)
aRatio    = array.array('d', Ratio)
aRatioErr = array.array('d', RatioErr)
aZero     = array.array('d', Zero)

grRatio = r.TGraphErrors(len(Ratio),grData.GetX(),aRatio,aZero,aRatioErr)
MaxRatio = r.TMath.MaxElement(grRatio.GetN(),grRatio.GetY())
MinRatio = r.TMath.MinElement(grRatio.GetN(),grRatio.GetY())

if(abs(MaxRatio-1) > abs(MinRatio-1)):
    MinRatio = max(2. - MaxRatio, 0.)
else:
    MaxRatio = 2. - MinRatio

grRatio.SetTitle("")
grRatio.SetMarkerColor(r.kBlack)
grRatio.SetMarkerSize(2.5)
grRatio.SetMarkerStyle(8)
grRatio.GetXaxis().SetTitle("Tile Thickness (cm)")
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
Ratio_allErr.Draw("E2same")


c.SaveAs("Data_vs_Simulation_Width_" + Samples +".pdf")
