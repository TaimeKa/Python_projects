#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""Calculate manipulation co-occurences"""

# On each patient specialist performs several medical manipulations.
# Code checks how often each 2 manipulations occur together in medical records of one specialist.

#%%
# read data from excel
data = pd.read_excel('data_02_manip_cooccurence.xlsx')

#%%
# filter specialist and manipulations I want to check
manip_list = ['M3452', 'M3487', 'M3655', 'M3445', 'M3424', 'M3438', 'M3459', 'M3494', 'M3466', 'M3473', 'M3501', 'M3557', 'M3620', 'M3669']
spec_name = 'Jesse Simpson'
 
data_doctor = data[(data.specialist_name==spec_name) & (data.manipulation_code.isin(manip_list))]

# %%
# crosstable - does manipulation from list appears in medical record
data_doctor_cross = pd.crosstab(data_doctor['medical_record_id'], data_doctor['manipulation_code']).astype(bool)
# convert to int for calcuations
data_doctor_cross = data_doctor_cross.astype(int)

#%%
# this step is necessary to create crosstable with all manipulation columns from manipulation list (even if a
# specialist didn't use every manipulation), for comparison between different specialists.
df_empty = pd.DataFrame(index = data_doctor_cross.index, columns = manip_list)
df_combined = df_empty.combine_first(data_doctor_cross)
df_combined = df_combined.fillna(0)

#%%
# dot product to calculate co-occurence
doctor_dot = df_combined.T.dot(df_combined)
np.fill_diagonal(doctor_dot.values, 0)

# normalize co-occurence matrix to compare results between different specialists, because specialists
# have different number of medical records
doctor_dot = doctor_dot/len(data_doctor_cross) #divide by number of medical records

#%%
"""Draw co-occurence heatmanp"""
ax = sns.heatmap(doctor_dot, cmap="YlGnBu", vmin = 0, vmax = 1.1, linecolor='gray', linewidths=.5)
ax.set_title('Proportion of manipulation co-occurence in consulations with specialist {}'.format(spec_name))
plt.savefig('Co-occurence_{}.png'.format(spec_name), dpi = 400, bbox_inches="tight")

# %%
