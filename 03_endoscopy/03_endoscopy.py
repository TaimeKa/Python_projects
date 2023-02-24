
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import dfply as ply

#%%
# read data from excel
data = pd.read_excel('data_03_endoscopy.xlsx')

# %%
"""Endoscopy with/without anesthesia"""

# Although endoscopy with anesthesia is publicly funded, some clinics make patients pay for anesthesia.
# Data contains endoscopy and anesthesia manipulations (local, total and sedation) what are publicly funded. 
# This code checks, if cases with endoscopy manipulations contain anesthesia manipulations. 
# If anesthesia manipulation is not present, most probably clinic made patient pay for anesthesia. 

#%%
"""Assign catogory based on manipulation code"""

#create a list with each category of manipulations

# endoscopy manipulations
endoscopy_manip=['M3752', 'M3960', 'M3986', 'M4012', 'M4233', 'M4324', 'M4454', 'M4623', 'M4506',  'M4883'] 
#local anesthesia manipulations
local_anesthesia_manip=['M3778']
#total anesthesia or sedation manipulations
total_anesthesia_manip=['M4051', 'M3869', 'M3895', 'M4311', 'M4298', 'M3804', 'M4142']

#convert lists to one dictionary
manip_cat_dict = {i:'endo' for i in endoscopy_manip} | {i:'loc_a' for i in local_anesthesia_manip} | {i:'tot_a' for i in total_anesthesia_manip}

#apply dictionary to manipulation code column. Assign 'endo', 'loc_a' or 'tot_a' based on manip. code
data['manipulation_category'] = data['manipulation_code'].map(manip_cat_dict)


# %%
"""Define functions to calculate occurrences in each category"""
#function to calculate how many specific occurrences are in the column.

def count_endo(x):
    return (x=='endo').sum()

def count_loc_a(x):
    return (x=='loc_a').sum()

def count_tot_a(x):
    return (x=='tot_a').sum()

#%%
"""group by case"""
#group by case, case consist of one or several medical records with same patient, same health center and start date

data_patient = (data.groupby(['medical_record_start_date', 'health_center_id', 'patient_id'], dropna=False)
.agg(
medical_record_id = ('medical_record_id', set),
health_center_name = ('health_center_name', 'first'),
specialist_id= ('specialist_id', set),
specialist_name = ('specialist_name', set),
endo_manip_sum = ('manipulation_category', count_endo), #count "endo" occurrences in manipulation category, using function
loc_a_manip_sum = ('manipulation_category', count_loc_a),
tot_a_manip_sum = ('manipulation_category', count_tot_a)
))

data_patient = data_patient.reset_index()

#filter cases, where endoscopic manipulation was performed
data_patient_endo = data_patient[data_patient.endo_manip_sum>0]

# New colomn with "TRUE" if case contains any of anesthesia manipulations 
data_patient_endo['any_anesthesia'] = ((data_patient_endo.loc_a_manip_sum>0) |  (data_patient_endo.tot_a_manip_sum>0))

# %%
"""group by clinic"""
# summary, how many cases without anesthesia each clinic has. 

#function to calculate how many specific occurrences are in the column.
def count_false(x):
    return (x==0).sum()

def count_true(x):
    return (x==1).sum()

data_hospitals = (data_patient_endo.groupby('health_center_id')
.agg(health_center_name = ('health_center_name', 'first'),
n_cases_total = ('any_anesthesia', 'count'),
n_cases_with_anesthesia = ('any_anesthesia',  count_true), #count "TRUE" occurrences using function
n_cases_without_anesthesia = ('any_anesthesia',  count_false)
))

# %%
# export data
temp = pd.ExcelWriter('output_03_endoscopy.xlsx')
data_patient_endo.to_excel(temp, sheet_name='cases')
data_hospitals.to_excel(temp, sheet_name='summary_hospitals')
temp.save()
# %%
