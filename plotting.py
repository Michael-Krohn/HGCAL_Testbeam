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


############# data Arrays ##############

#Breakdown Voltages of both SIPMS used
Breakdown_s13360 = 51.76
Breakdown_s14160 = 38.31

### Over Voltages ###
#Jan s14160 Over voltages
J14_Over  = [40.83, 41.33, 41.83, 42.33, 42.83] - Breakdown_s14160
#Feb s13360 Over voltages
F13_Over  = [53.26, 53.76, 54.26, 54.76, 55.26] - Breakdown_s13360
#Feb s14160 Over Voltages
F14_Over  = [41.83, 42.31, 42.81] - Breakdown_s14160

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


############################################
if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print "Please use J14_MPV, J14_Gain, F13_MPV, F13_Gain, F14_MPV, or F14_Gain as an argument"
    exit(0)
elif len(sys.argv) == 1:
    print "Please use J14_MPV, J14_Gain, F13_MPV, F13_Gain, F14_MPV, or F14_Gain as an argument"
    exit(0)

Samples = sys.argv[1]
if Samples != "J14_MPV" and Samples != "J14_Gain" and Samples != "F13_MPV" and Samples != "F13_Gain" and Samples != "F14_MPV" and Samples != "F14_Gain":
    print "Please use J14_MPV, J14_Gain, F13_MPV, F13_Gain, F14_MPV, or F14_Gain as an argument"
    exit(0)


### Creating Graphs ###
if Samples == "J14_Gain":
    grData = r.TGraphErrors(len(J14_Gain),J14_Over,J14_Gain,0.005,J14_Gainer)
    grData.GetYaxis().SetTitle("Gain (PE/adc)")
    
elif Samples == "J14_MPV":
    grData = r.TGraph(len(J14_MPV),J14_Over,J14_MPV)
    grData.GetYaxis().SetTitle("MPV (PE)")
    
elif Samples == "F13_Gain":
    grData = r.TGraphErrors(len(F13_Gain),F13_Bias,F13_Gain,0.005,F13_Gainer)
    grData.GetYaxis().SetTitle("Gain (PE/adc)")
    
elif Samples == "F13_MPV":
    grData = r.TGraph(len(F13_MPV),F13_Over,F13_MPV)
    grData.GetYaxis().SetTitle("MPV (PE)")

elif Samples == "F14_Gain":
    grData = r.TGraphErrors(len(F14_Gain),F14_Bias,F14_Gain,0.005,F14_Gainer)
    grData.GetYaxis().SetTitle("Gain (PE/adc)")
    
elif Samples == "F14_MPV":
    grData = r.TGraph(len(F14_MPV),F14_Over,F14_MPV)
    grData.GetYaxis().SetTitle("MPV (PE)")


grData.SetTitle("")
grData.SetMarkerColor(r.kRed)
grData.SetLineColor(r.kRed)
grData.SetMarkerSize(2.5)
grData.SetMarkerStyle(32)
grData.GetXaxis().SetTitle("Over Voltage (Volts)")
grData.GetYaxis().SetRangeUser(0, 1.7*grMax)
grData.GetXaxis().SetLabelSize(0)
grData.GetYaxis().SetTitleSize(.2*3/7)
grData.GetYaxis().SetLabelSize(.2*3/7)

grData.SetMarkerColor(r.kBlack)
grData.SetMarkerSize(2.5)
grData.SetMarkerStyle(8)

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