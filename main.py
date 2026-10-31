import shutil
import pandas as pd
import os
import numpy as np

from cairnopen import *

app_home = os.getcwd()


# préparation du répertoire pour la simulation
simuPath = os.path.join(app_home, './results')
dataPath = os.path.join(app_home, './data')

if os.path.exists(simuPath):
	shutil.rmtree(simuPath)
os.makedirs(simuPath)

simuFile = 'First_Model.json'
simuFull = os.path.join(simuPath, simuFile)
shutil.copy(os.path.join(dataPath, simuFile), simuFull)

cairn_instance = CairnAPI(True)


print(simuFull)
problem = cairn_instance.read_study(simuFull)

# Import des timeseries
problem.add_timeseries(os.path.join(dataPath, 'conso_foyer_4pers_dataseries.csv'))
problem.add_timeseries(os.path.join(dataPath, 'prod_pv_par_m2_dataseries.csv'))


listEV = problem.energy_carriers
for EVname in listEV:
    EV = problem.get_energy_carrier(EVname)
    print(f"{EV.name} is an EnergyVector of type {EV.type}")
    print(f"{EV.name} settings:")
    for i in range(0, len(EV.settings), 8):
        chunk = EV.settings[i:i + 8]
        print(', '.join(map(str, chunk)))
    print("")
    print(f"{EV.name} mandatory settings:")
    for i in range(0, len(EV.settings[CairnAPI.ESettingsLimited.mandatory]), 9):
        chunk = EV.settings[CairnAPI.ESettingsLimited.mandatory][i:i + 9]
        print(', '.join(map(str, chunk)))
    print("")
    print("With the value of each setting:")
    setEV = EV.setting_values
    for i in setEV:
        print(f"{i} : {setEV[i]}")
    print("")
    print("Retrieving the value of one particular parameter:")
    value = EV.get_setting_value("IsFuelCarrier")
    print(f"Is fuel carrier? {value}")
    print("")


list_bus = problem.buses
print(list_bus)

list_compo = problem.get_components()
print(list_compo)

# compo = problem.get_component("ELY_PEM")
# print(compo.name)
# df = pd.DataFrame.from_dict(compo.setting_values, orient='index')
# print(df)
# print("")
# print("Retrieving the value of a given parameter:")
# value = compo.get_setting_value("Capex")
# print(f"Capex : {value}")