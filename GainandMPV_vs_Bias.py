import ROOT as r
import sys
import datetime
import subprocess
import os
import copy
# import sets
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


############# data Arrays ##############

#Breakdown Voltages of both SIPMS used
Breakdown_s13360 = 51.76
Breakdown_s14160 = 38.31

### Over Voltages ###
#Jan s14160 Over voltages
J14_Over  = [40.83, 41.33, 41.83, 42.33, 42.83]
#Feb s13360 Over voltages
F13_Over  = [53.26, 53.76, 54.26, 54.76, 55.26]
#Feb s14160 Over Voltages
F14_Over  = [41.83, 42.31, 42.81]

for i in range(5):
    J14_Over[i] = J14_Over[i]-Breakdown_s14160
    F13_Over[i] = F13_Over[i]-Breakdown_s13360
for i in range(3):
    F14_Over[i] = F14_Over[i]-Breakdown_s14160
    
### Over Voltage error ###
J14_Overer  = [0.005, 0.005, 0.005, 0.005, 0.005]
F13_Overer  = [0.005, 0.005, 0.005, 0.005, 0.005]
F14_Overer  = [0.005, 0.005, 0.005]

### MPV of Light Yield Distributions ###
J14_MPV   = [28.48, 30.04, 33.23, 35.41, 36.00]
F13_MPV   = [24.94, 28.27, 33.38, 37.80, 38.41]
F14_MPV   = [29.68, 31.03, 31.34]

### SIPM Gain ###
J14_Gain = [0.130 , 0.150 , 0.168 , 0.195 , 0.216]
F13_Gain = [0.088, 0.124, 0.148, 0.175, 0.213]
F14_Gain = [0.159, 0.183, 0.201]

### SIPM Gain Error ###
J14_Gainer = [0.003, 0.002, 0.002, 0.004, 0.004]
F13_Gainer = [0.002, 0.002, 0.003, 0.003, 0.004]
F14_Gainer = [0.002, 0.002, 0.002]

J14_Over    = array.array('d', J14_Over)
F13_Over    = array.array('d', F13_Over)
F14_Over    = array.array('d', F14_Over)

J14_Overer    = array.array('d', J14_Overer)
F13_Overer    = array.array('d', F13_Overer)
F14_Overer    = array.array('d', F14_Overer)

J14_MPV    = array.array('d', J14_MPV)
F13_MPV    = array.array('d', F13_MPV)
F14_MPV    = array.array('d', F14_MPV)

J14_Gain    = array.array('d', J14_Gain)
F13_Gain    = array.array('d', F13_Gain)
F14_Gain    = array.array('d', F14_Gain)

J14_Gainer   = array.array('d', J14_Gainer)
F13_Gainer    = array.array('d', F13_Gainer)
F14_Gainer    = array.array('d', F14_Gainer)

############################################
if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("Please use J14_MPV, J14_Gain, F13_MPV, F13_Gain, F14_MPV, or F14_Gain as an argument")
    exit(0)
elif len(sys.argv) == 1:
    print("Please use J14_MPV, J14_Gain, F13_MPV, F13_Gain, F14_MPV, or F14_Gain as an argument")
    exit(0)

Samples = sys.argv[1]
if Samples != "J14_MPV" and Samples != "J14_Gain" and Samples != "F13_MPV" and Samples != "F13_Gain" and Samples != "F14_MPV" and Samples != "F14_Gain":
    print("Please use J14_MPV, J14_Gain, F13_MPV, F13_Gain, F14_MPV, or F14_Gain as an argument")
    exit(0)

### Creating Graphs ###
if Samples == "J14_Gain":
    grData = r.TGraphErrors(len(J14_Gain),J14_Over,J14_Gain,J14_Overer,J14_Gainer)
    grMax  = r.TMath.MaxElement(grData.GetN(),grData.GetY())
    grMin  = r.TMath.MinElement(grData.GetN(),grData.GetY())
    grData.GetYaxis().SetTitle("Gain (PE/adc)")
    
elif Samples == "J14_MPV":
    grData = r.TGraph(len(J14_MPV),J14_Over,J14_MPV)
    grMax  = r.TMath.MaxElement(grData.GetN(),grData.GetY())
    grMin  = r.TMath.MinElement(grData.GetN(),grData.GetY())
    grData.GetYaxis().SetTitle("MPV (PE)")
    
elif Samples == "F13_Gain":
    grData = r.TGraphErrors(len(F13_Gain),F13_Bias,F13_Gain,F13_Overer,F13_Gainer)
    grMax  = r.TMath.MaxElement(grData.GetN(),grData.GetY())
    grMin  = r.TMath.MinElement(grData.GetN(),grData.GetY())
    grData.GetYaxis().SetTitle("Gain (PE/adc)")
    
elif Samples == "F13_MPV":
    grData = r.TGraph(len(F13_MPV),F13_Over,F13_MPV)
    grMax  = r.TMath.MaxElement(grData.GetN(),grData.GetY())
    grMin  = r.TMath.MinElement(grData.GetN(),grData.GetY())
    grData.GetYaxis().SetTitle("MPV (PE)")

elif Samples == "F14_Gain":
    grData = r.TGraphErrors(len(F14_Gain),F14_Bias,F14_Gain,F14_Overer,F14_Gainer)
    grMax  = r.TMath.MaxElement(grData.GetN(),grData.GetY())
    grMin  = r.TMath.MinElement(grData.GetN(),grData.GetY())
    grData.GetYaxis().SetTitle("Gain (PE/adc)")
    
elif Samples == "F14_MPV":
    grData = r.TGraph(len(F14_MPV),F14_Over,F14_MPV)
    grMax  = r.TMath.MaxElement(grData.GetN(),grData.GetY())
    grMin  = r.TMath.MinElement(grData.GetN(),grData.GetY())
    grData.GetYaxis().SetTitle("MPV (PE)")

grData.SetTitle("")
grData.SetMarkerColor(r.kBlack)
grData.SetMarkerSize(2.5)
grData.SetMarkerStyle(8)
grData.GetXaxis().SetTitle("Over Voltage (Volts)")
grData.GetYaxis().SetRangeUser(0.7*grMin,1.2*grMax)
grData.GetXaxis().SetLabelSize(0.06)
# grData.GetYaxis().SetTitleSize(.2*3/7)
grData.GetYaxis().SetLabelSize(0.06)

### Creating Canvas ###
c = r.TCanvas("c","c",1000,1000)
c.SetFillColor(0)
# c.SetBorderMode(0)
# c.SetBorderSize(2)
# c.SetFrameBorderMode(0)
grData.Draw("AP")

CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.cd()
c.Update()
c.RedrawAxis()
frame = c.GetFrame()
frame.Draw()

###### fitting Gain Data ######
if Samples == "F14_Gain" or Samples == "J14_Gain" or Samples == "F14_Gain":
    func = r.TF1('func', '[0] + [1]*x', 0, 5)
    Fit = grData.Fit('func', 'S')
    legend = r.TLegend(0.2,0.7,0.48,0.9)
    legend.SetFillStyle(0)
    legend.SetBorderSize(1)
    legend.SetTextSize(0.065)
    legend.SetTextFont(42)
    legend.AddEntry(grData, "Data", "PE")
    legend.AddEntry(func, "Data Fit", "L")
    legend.Draw()
    

c.SaveAs("plots/" + Samples + "_vs_OverVoltage.pdf")