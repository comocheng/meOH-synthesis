import os
from random import randint
import pandas as pd
import numpy as np
import csv
import cantera as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
%matplotlib inline

import seaborn
plt.style.use('seaborn-white')
from pathlib import Path
import time

import matplotlib.cm as cm
from IPython.display import Image
from rmgpy import chemkin

###############################################################################
# # plotting functions
###############################################################################
def plot_rates_grabow(df):
    '''
    This function returns a 2x2 set of charts like the ones above, 
    for comparison with the grabow rates and coverages. 
    df - dataframe to load
    labels - list of labels to use. first is the "x" values, then the y
    '''
    h2_mol = [0.5, 0.75, 0.8, 0.95]
    grabow_labels = [
        "Methanol Production",
        "Water-Gas Shift",
        "CO Hydrogenation",
        "CO2 Hydrogenation",
        "H2O Production",]
    
    h2_label = "y(H2)"
    co_co2_label = "CO2/(CO+CO2)"
    fig, ax = plt.subplots(2,2,figsize=(15,15))
    
    axes = [(0,0), (0,1), (1,0), (1,1)]
    
    color_dict = { 0:"k", 1:"y", 2:"g", 3:"b", 4:"r"}

    for coord,h2 in enumerate(h2_mol):
        
        for color,label in enumerate(grabow_labels):
            # "slot" where we place chart
            slot = axes[coord]
            df[np.isclose(df["y(H2)"], h2)].plot(x=co_co2_label,
                                                 y=label,
                                                 ax=ax[slot], 
                                                 color=color_dict[color],
                                                )
            ax[slot].set_title(f'mole frac H2 = {h2}')
            ax[slot].autoscale(enable=True, axis='y')
            ax[slot].set_ylabel("Turn over frequency ($s^{-1}$)")
    
    return fig

def plot_rates_rmg(df):
    '''
    This function returns a 2x2 set of charts like the ones above, 
    for comparison with the grabow rates and coverages. 
    df - dataframe to load
    labels - list of labels to use. first is the "x" values, then the y
    '''
    
    h2_mol = [0.5, 0.75, 0.8, 0.95]
    # this part is tricky. 
    
    #         "Methanol Production"  :  CH3O* + H* -> CH3OH* + *
    #         "Water-Gas Shift"      :  OH* + CO* -> COOH* + *
    #         "CO Hydrogenation"     :  CO* + H* -> HCO* + *
    #         "CO2 Hydrogenation"    :  CO2* + H* -> HCO2* + *
    #         "H2O Production"       :  #1 - #2
    #                                   #1:  H2O*+*->OH*+H*
    #                                   #2:  COOH* + OH* -> CO2* + H2O*
    rmg_labels = [
        "Methanol TOF ($s^{-1}$)",
        "WGS Reaction TOF ($s^{-1}$)",
        "CO Hydrogenation TOF ($s^{-1}$)",
        "CO2 Hydrogenation TOF ($s^{-1}$)",
        "H2O TOF ($s^{-1}$)",
    ]
        
    h2_label = "x_H2 initial"
    co_co2_label = "CO2/(CO2+CO)"
    color_dict = { 0:"k", 1:"y", 2:"g", 3:"b", 4:"r"}
    fig, ax = plt.subplots(2,2,figsize=(15,15))
    axes = [(0,0), (0,1), (1,0), (1,1)]

    for coord,h2 in enumerate(h2_mol):
        
        for color,label in enumerate(rmg_labels):
            # "slot" where we place chart
            slot = axes[coord]
            df[np.isclose(df[h2_label], h2)].plot(x=co_co2_label,
                                                 y=label,
                                                 ax =ax[slot], 
                                                 color=color_dict[color],
                                                )
            ax[slot].set_title(f'mole frac H2 = {h2}')
            ax[slot].autoscale(enable=True, axis='y')
            ax[slot].set_ylabel("Turn over frequency ($s^{-1}$)")
    
    return fig

def plot_covs_grabow(df):
    '''
    This function returns a 2x2 set of charts like the ones above, 
    for comparison with the rmg rates and coverages. 
    df - dataframe to load
    '''
    
    h2_mol = [0.5, 0.75, 0.8, 0.95]
    grabow_labels = [
        "vacant",
        "HCOO",
        "CH3O",
        "H",
        "OH",
    ]
    
    h2_label = "y(H2)"
    co_co2_label = "CO2/(CO+CO2)"
    fig, ax = plt.subplots(2,2,figsize=(15,15))
    
    axes = [(0,0), (0,1), (1,0), (1,1)]
    
    color_dict = { 0:"k", 1:"y", 2:"g", 3:"b", 4:"r"}

    for coord,h2 in enumerate(h2_mol):
        
        for color,label in enumerate(grabow_labels):
            # "slot" where we place chart
            slot = axes[coord]
            df[np.isclose(df["y(H2)"], h2)].plot(x=co_co2_label,
                                                 y=label,
                                                 ax=ax[slot], 
                                                 color=color_dict[color],
                                                )
            ax[slot].set_title(f'mole frac H2 = {h2}')
            ax[slot].autoscale(enable=True, axis='y')
            ax[slot].set_ylabel("site fraction")
            
    return fig

def plot_covs_rmg(df, labels, gas=False):
    '''
    This function returns a 2x2 set of charts like the ones above, 
    for comparison with the grabow rates and coverages. 
    df - dataframe to load
    labels - list of labels to use. first is the "x" values, then the y
    '''
    
    h2_mol = [0.5, 0.75, 0.8, 0.95]
    
    rmg_labels = labels
        
    h2_label = "x_H2 initial"
    co_co2_label = "CO2/(CO2+CO)"
    color_dict = { 0:"k", 1:"y", 2:"g", 3:"b", 4:"r", 5:"deeppink"}
    fig, ax = plt.subplots(2,2,figsize=(15,15))
    axes = [(0,0), (0,1), (1,0), (1,1)]

    for coord,h2 in enumerate(h2_mol):
        
        for color,label in enumerate(rmg_labels):
            # "slot" where we place chart
            slot = axes[coord]
            df[np.isclose(df[h2_label], h2)].plot(x=co_co2_label,
                                                 y=label,
                                                 ax =ax[slot], 
                                                 color=color_dict[color],
                                                )
            ax[slot].set_title(f'mole frac H2 = {h2}')
            ax[slot].autoscale(enable=True, axis='y')
            if gas: 
                ax[slot].set_ylabel("mole fraction")
            else: 
                ax[slot].set_ylabel("site fraction")
    return fig

###############################################################################
# Plotting grabow data vs rmg data
###############################################################################

# load file paths
rmg_model_path = "/work/westgroup/ChrisB/_01_MeOH_repos/meOH-synthesis/"

cantera_path = rmg_model_path + "base/cantera/"
cti_file = cantera_path + "chem_annotated.cti"

gas = ct.Solution(cti_file)
surface = ct.Interface(cti_file, "surface1", [gas])

model_dict_file = rmg_model_path + "base/chemkin/species_dictionary.txt"
grabow_dict_file = "./species_data/species_dictionary.txt"

# create chemkin species_dicts
model_dict = chemkin.load_species_dictionary(model_dict_file)
grabow_dict = chemkin.load_species_dictionary(grabow_dict_file)

# make a dictionary to "translate" the names from the grabow model to ours
# irrespective of the naming convention.
spc_trans = {}
for name, entry in model_dict.items(): 
    for g_name, g_entry in grabow_dict.items():
        if entry.is_isomorphic(g_entry):
            # remove (#) so it is neater
            g_name_new = g_name.split("(", 1)[0]
            spc_trans.update({g_name_new :name})

# read in dataframe for run. split into grabow and graaf data
data_all = pd.read_csv(cantera_path+ "ct_analysis.csv")
data_graaf = data_all[data_all['experiment'] == "graaf_1988"]
data_grab = data_all[data_all['experiment'] == "grabow2011"]

# get what label is for co/co2 ratio column
co_co2_label = "CO2/(CO2+CO)"

# setup up the column label strings for rop
rop_str = " ROP [kmol/m^2 s]"     

# load in the TOFs for methanol
ch3oh_dict = {}  
        
for rxn in surface.reactions():
    if spc_trans["CH3OH"] in rxn.equation: 
        rxn_string = rxn.equation + rop_str
        if spc_trans["CH3OH"] in rxn.product_string:
            print(rxn_string, "forward")
            ch3oh_dict.update({rxn_string:1})
        elif spc_trans["CH3OH"] in rxn.reactant_string: 
            print(rxn_string, "reverse")
            ch3oh_dict.update({rxn_string:-1})

data_grab["Methanol TOF ($s^{-1}$)"] = 0 #(initialize)
for rxn, direct in ch3oh_dict.items():
    if direct == 1:
        data_grab["Methanol TOF ($s^{-1}$)"] += data_grab[rxn]/surface.site_density
    elif direct == -1:
        data_grab["Methanol TOF ($s^{-1}$)"] -= data_grab[rxn]/surface.site_density

# load in data for WGS rxn
wgs_hyd_dict = {}
# for rxn in surface.reactions():
# #     if spc_trans["CO*"] in rxn.reactant_string and spc_trans["OH*"] in rxn.reactant_string:
#     if spc_trans["CO2*"] in rxn.reactant_string and spc_trans["COOH*"] in rxn.product_string:
#         rxn_string = rxn.equation + rop_str
#         print(rxn.equation, "forward")
#         wgs_hyd_dict.update({rxn_string:-1})
#     elif spc_trans["COOH*"] in rxn.reactant_string and spc_trans["CO2*"] in rxn.product_string:
#         rxn_string = rxn.equation + rop_str
#         print(rxn.equation, "forward")
#         wgs_hyd_dict.update({rxn_string:1})

# # hardcode HOX(19) + OCX(17) <=> HOCXO(23) + X(1) for now just to analyze
wgs_hyd_dict.update(
    {f'{spc_trans["CO*"]} + {spc_trans["OH*"]} <=> {spc_trans["COOH*"]} + {spc_trans["X"]}{rop_str}':1
#     {f'{spc_trans["H2O*"]} + {spc_trans["X"]} <=> {spc_trans["H*"]} + {spc_trans["OH*"]}{rop_str}':1 
#     {f'{spc_trans["CO*"]} + {spc_trans["OH*"]} <=> {spc_trans["COOH*"]} + {spc_trans["X"]}{rop_str}':1
    }
)

data_grab["WGS Reaction TOF ($s^{-1}$)"] = 0 #(initialize)
for rxn, direct in wgs_hyd_dict.items():
    if direct == 1:
        data_grab["WGS Reaction TOF ($s^{-1}$)"] += data_grab[rxn]/surface.site_density
    elif direct == -1:
        data_grab["WGS Reaction TOF ($s^{-1}$)"] -= data_grab[rxn]/surface.site_density


# load in CO hydrogenation data 
co_hyd_dict = {}
rop_str = " ROP [kmol/m^2 s]"
for rxn in surface.reactions():
    if spc_trans["CO*"] in rxn.equation and spc_trans["HCO*"] in rxn.equation: 
        rxn_string = rxn.equation + rop_str
        if spc_trans["CO*"] in rxn.reactant_string and not spc_trans["HCO*"] in rxn.reactant_string:
            print(rxn.equation, "forward")
            co_hyd_dict.update({rxn_string:1})
        elif spc_trans["CO*"] in rxn.product_string and not spc_trans["HCO*"] in rxn.product_string: 
            print(rxn.equation, "reverse")
            co_hyd_dict.update({rxn_string:-1})

data_grab["CO Hydrogenation TOF ($s^{-1}$)"] = 0 #(initialize)
for rxn, direct in co_hyd_dict.items():
    if direct == 1:
        data_grab["CO Hydrogenation TOF ($s^{-1}$)"] += data_grab[rxn]/surface.site_density
    elif direct == -1:
        data_grab["CO Hydrogenation TOF ($s^{-1}$)"] -= data_grab[rxn]/surface.site_density

# load in CO2 hydrogenation data
co2_hyd_dict = {}
for rxn in surface.reactions():
    if spc_trans["CO2*"] in rxn.equation and spc_trans["HCOO*"] in rxn.equation: 
        rxn_string = rxn.equation + rop_str
        if spc_trans["CO2*"] in rxn.reactant_string and not spc_trans["HCOO*"] in rxn.reactant_string:
            print(rxn.equation, "forward")
            co2_hyd_dict.update({rxn_string:1})
        elif spc_trans["CO2*"] in rxn.product_string and not spc_trans["HCOO*"] in rxn.product_string: 
            print(rxn.equation, "reverse")
            co2_hyd_dict.update({rxn_string:-1})

data_grab["CO2 Hydrogenation TOF ($s^{-1}$)"] = 0 #(initialize)
for rxn, direct in co2_hyd_dict.items():
    if direct == 1:
        data_grab["CO2 Hydrogenation TOF ($s^{-1}$)"] += data_grab[rxn]/surface.site_density
    elif direct == -1:
        data_grab["CO2 Hydrogenation TOF ($s^{-1}$)"] -= data_grab[rxn]/surface.site_density

# load in H2O ROP data
h2o_dict = {}        
for rxn in surface.reactions():
    if spc_trans["H2O"] in rxn.equation: 
        rxn_string = rxn.equation + rop_str
        if spc_trans["H2O"] in rxn.reactant_string:
            print(rxn.equation, "reverse")
            h2o_dict.update({rxn_string:-1})
        elif spc_trans["H2O"] in rxn.product_string: 
            print(rxn.equation, "forward")
            h2o_dict.update({rxn_string:1}) 

data_grab["H2O TOF ($s^{-1}$)"] = 0 #(initialize)
for rxn, direct in h2o_dict.items():
    if direct == 1:
        data_grab["H2O TOF ($s^{-1}$)"] += data_grab[rxn]/surface.site_density
    elif direct == -1:
        data_grab["H2O TOF ($s^{-1}$)"] -= data_grab[rxn]/surface.site_density

# get surface site density on a molar basis (do we need this?)
surface.site_density
site_dens_mol = surface.site_density*1e-3
site_dens_mol

# load in grabow data
Grabow_rates = pd.read_csv("./paper_data/Grabow_rates.csv")
Grabow_cov = pd.read_csv("./paper_data/Grabow_coverages.csv")

# plot rates
fig_grab_rates = plot_rates_grabow(Grabow_rates)
fig_rmg_rates = plot_rates_rmg(data_grab[data_grab["T (K)"] == 528])

# plot coverages
fig_grab_cov = plot_covs_grabow(Grabow_cov)

labels = [
    spc_trans["CO"],
    spc_trans["CO2"],
    spc_trans["H2O"],
    spc_trans["CH3OH"],
    spc_trans["H2"],
]
fig_rmg_cov = plot_covs_rmg(data_grab[data_grab["T (K)"] == 528], labels, gas=True)


# save figures in a report
pp = PdfPages('report.pdf')
pp.savefig(fig_grab_rates)
pp.savefig(fig_rmg_rates)
pp.savefig(fig_grab_cov)
pp.savefig(fig_rmg_cov)
pp.close()