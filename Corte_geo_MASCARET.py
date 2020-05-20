# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:33:31 2020

@author: ICJRC
Obj: Extrac for .geo file other .geo file for MASCARET
"""
import pandas as pd
import numpy as np

# Abcsisse limits for extraction
AbsIni = 84100
AbsFin = 200000

# Files
Old_file = 'SEC_COR_TRPZ.geo'
New_file = 'SEC_COR_TRPZ_1.geo'

# Heating model
x = 500
AbsIni = AbsIni - x
AbsFin = AbsFin + x

# Original data
db = pd.read_csv(Old_file, header = None)

# Extrac Axis
dif = db[db[0].str.contains('PROFIL')].copy()
dif = dif[0].str.split(expand = True).copy()
Abs = pd.to_numeric(dif[3])

AbsIniObs = Abs - AbsIni
AbsIniObs = max(Abs[AbsIniObs <= 0])

AbsFinObs = Abs - AbsFin
AbsFinObs = Abs[AbsFinObs >= 0].iloc[1]

IdIni = dif[dif[3] == str(AbsIniObs)].copy().index[0]
IdFin = dif[dif[3] == str(AbsFinObs)].copy().index[0]

db_r  = db.loc [IdIni : IdFin - 1].copy()
dif_r = dif.loc[IdIni : IdFin - 1].copy()

jj = 0

# Replace with a new profile mark
for ii in np.linspace(1, len(dif_r), len(dif_r)):    
    dif_r[2].iloc[jj] = 'P' + str(int(ii))
    jj += 1
    
dif_r[0] = dif_r[0].astype(str) + " " + dif_r[1].astype(str) + " " + dif_r[2].astype(str) + " " + (dif_r[3].astype(int) - int(dif_r[3].iloc[0])).astype(str) 

# Replace profile format in the print dataframe
for ii in dif_r.index:
    db_r[0].loc[ii] = dif_r[0].loc[ii]

db_r = db_r.reset_index()

# Print new file
db_r[0].to_csv(New_file, header = False, index = False)

# Print help file
n = []
N = pd.DataFrame()
n.append( 'Number of profiles: ' + str(len(dif_r)))
N[0] = n
N.to_csv('help_file.txt', header = False, index = False)
