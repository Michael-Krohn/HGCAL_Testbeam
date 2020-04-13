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
Time   = [11, 13, 15, 20, 25, 30, 35, 40, 45, 50, 60]

aTime  = array.array('d', Time)

### Simulation Results ###
Amp  = [1, 0.7, 0.4, 0.3, 0.21, 0.14, 0.1, 0.06, 0.05, 0.03, 0.01]

aAmp = array.array('d', Amp)

############################################

### Plotting ###
grSimulation = r.TGraph(len(aTime),aTime, aAmp)


grSimulation.SetTitle("")
grSimulation.SetMarkerColor(r.kRed)
grSimulation.SetLineColor(r.kRed)
grSimulation.SetMarkerSize(2.5)
grSimulation.SetMarkerStyle(32)
grSimulation.GetXaxis().SetTitle("Time (ns)")
grSimulation.GetYaxis().SetTitle("Amplitude (a.u.)")
#grSimulation.GetYaxis().SetRangeUser(0, 1.5*grMax)

c = r.TCanvas("c","c",1000,1000)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetBorderSize(2)
c.SetFrameBorderMode(0)

grSimulation.Draw("AP")

simFit = r.TF1("simFit","expo",14,50)
grSimulation.Fit("simFit", "RQ")

norm = simFit.GetParameter(0)
decayConst = simFit.GetParameter(1)
timeConst = -1./decayConst

print "timeConst: ", timeConst

#CMS_lumi.CMS_lumi(c, iPeriod, iPos)
#c.cd()
#c.Update()
#c.RedrawAxis()
#frame = c.GetFrame()
#frame.Draw()

c.SaveAs("JimsPulseShape.pdf")
#c.SaveAs("Data_vs_Simulation_HoleSize_" + Samples +".png")
