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


### Tile Sizes ###
TileWidths  = [3.8, 7.6, 11.4]

TileWidths_Err   = [0, 0, 0]

aTileWidths     = array.array('d', TileWidths)
aTileWidths_Err = array.array('d', TileWidths_Err)

### Simulation Results ###

simNorm = 0.548

nSimEvents = 4900.
SimVsWidth_Tyvek3x3     = [31.532, 37.8435, 43.4664]
SimVsWidth_Tyvek3x3_Err = [0.0819246, 0.0849135, 0.0911191]
SimVsWidth_Tyvek3x3     = simNorm*np.array(SimVsWidth_Tyvek3x3)
SimVsWidth_Tyvek3x3_Err = simNorm*np.array(SimVsWidth_Tyvek3x3_Err)

SimVsWidth_ESR3x3     = [33.3109, 46.0883, 52.82]
SimVsWidth_ESR3x3_Err = [0.0825699, 0.0960911, 0.101286]
SimVsWidth_ESR3x3     = simNorm*np.array(SimVsWidth_ESR3x3)
SimVsWidth_ESR3x3_Err = simNorm*np.array(SimVsWidth_ESR3x3_Err)

SimVsWidth_Tyvek4x4     = [21.7595, 24.1535, 26.8235]
SimVsWidth_Tyvek4x4_Err = [0.0652771, 0.0672232, 0.0709098]
SimVsWidth_Tyvek4x4     = simNorm*np.array(SimVsWidth_Tyvek4x4)
SimVsWidth_Tyvek4x4_Err = simNorm*np.array(SimVsWidth_Tyvek4x4_Err)

SimVsWidth_ESR4x4     = [23.199, 29.5625, 32.8976]
SimVsWidth_ESR4x4_Err = [0.0694875, 0.079565, 0.0800353]
SimVsWidth_ESR4x4     = simNorm*np.array(SimVsWidth_ESR4x4)
SimVsWidth_ESR4x4_Err = simNorm*np.array(SimVsWidth_ESR4x4_Err)

SimVsWidth_Tyvek5x5     = [16.0579, 16.6661, 18.0918]
SimVsWidth_Tyvek5x5_Err = [0.0541954, 0.0556745, 0.0593102]
SimVsWidth_Tyvek5x5     = simNorm*np.array(SimVsWidth_Tyvek5x5)
SimVsWidth_Tyvek5x5_Err = simNorm*np.array(SimVsWidth_Tyvek5x5_Err)

SimVsWidth_ESR5x5     = [17.2103, 20.8551, 22.3078]
SimVsWidth_ESR5x5_Err = [0.0581626, 0.0659629, 0.0689473]
SimVsWidth_ESR5x5     = simNorm*np.array(SimVsWidth_ESR5x5)
SimVsWidth_ESR5x5_Err = simNorm*np.array(SimVsWidth_ESR5x5_Err)


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

#DataVsWidth_Tyvek3x3     = [7.84, 9.17, 10.08]
DataVsWidth_Tyvek3x3     = [7.69, 9.74, 10.78]
#DataVsWidth_ESR3x3       = [25.95, 28.67, 43.28]
DataVsWidth_ESR3x3       = [25.53, 29.11, 44.3]
#DataVsWidth_Tyvek4x4     = [5.07, 8.42, 8.27]
DataVsWidth_Tyvek4x4     = [5.65, 8.12, 8.04]
#DataVsWidth_ESR4x4       = [16.59, 21.47, 21.17, 33.1]
DataVsWidth_ESR4x4       = [15.39, 20.67, 22., 32.37]
DataVsWidth_ESR4x4_all   = [15.39, 13.50, 20.67, 22., 15.43, 32.37]
#DataVsWidth_Tyvek5x5     = [4.34, 4.49, 5.41]
DataVsWidth_Tyvek5x5     = [4.38, 5.57, 5.37]
#DataVsWidth_ESR5x5       = [7.66, 15.91, 14.12, 16.15, 16.07]
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



### Normalizing Tyvek3x3 ###
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

