
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
data = pd.read_excel('data_05_comb.xlsx')

#%%
"""Combinations"""

#There are manipulations, which should not be combined in one medical record
#This code checks and prints out all incorrect combinations

# %%
# dictionary with incorrect combinations. Dict values should not be combined with key.
# values can be combined with each other

dictionary = {
'M3226':['M3198', 'M3177', 'M3016'],
'M3030':['M3128'],
'M0107':['M3058', 'M3016'],
'M3016':['M3058'],
'M3065':['M3107', 'M3058', 'M3226'],
'M3037':['M3044', 'M3051', 'M3254'],
'M3121':['M3044', 'M3051', 'M3254'],
'M3219':['M3233'],
'M3205':['M3233']
}

#%%
data_cross_all=pd.DataFrame()
  
for key, value in dictionary.items():
    value.append(key) 
    data_filter = data[data.manipulation_code.isin(value)] #on each iteration filter from data key and value manipulations

    data_cross = data_filter.pivot_table(index = ['medical_record_id', 'health_center_id', 'health_center_name', 'patient_id'], values = 'sum_manipulation',
    columns = 'manipulation_code', aggfunc='nunique', fill_value=0).reset_index()  #cross table for medical record and key, value

    data_cross.iloc[:,4:] = data_cross.iloc[:,4:].astype('bool').astype(int) # replace sum of manipulation with 0 and 1. 1 if manipulation is present, 0
    # 0 if manipulation is not present


    if key in data_cross.columns: #if cross table contain key manipulation (if data contain key manipulation)
        data_cross = data_cross[data_cross[key]>0] #filter medical records where key manipulation is present

        data_cross['sum'] = data_cross.iloc[:,4:].sum(axis=1) #sum number of distinct key, value manipulations in medical record

        data_cross_1 = data_cross[data_cross['sum']>1]  #filter medical records where sum ir >1. 
        #If sum ir 1, there is no combinations, only key manipulation is present
        
        data_cross_all = data_cross_all.append(data_cross_1) #combinenes results from all iterations 

        t = pd.ExcelWriter('output_' + str(key) + '_combinations.xlsx')
        data_cross.to_excel(t, sheet_name='Sheet1')
        data_cross_1.to_excel(t, sheet_name='Sheet2')
        t.save()

    else:
        print(key) # print key manipulation if cross table doesn't contain key manipulation
  
# %%
# incorrect medical record count summary for each health center
mr_count_summary = (data_cross_all >>  
ply.group_by(ply.X.health_center_id, ply.X.health_center_name) >>
ply.summarize(mr_count = ply.n(ply.X.medical_record_id)))

#%%
temp = pd.ExcelWriter('output_05_mr_per_hospital.xlsx')
mr_count_summary.to_excel(temp)
temp.save()

