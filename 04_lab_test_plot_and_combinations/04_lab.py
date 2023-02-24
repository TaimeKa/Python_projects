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
data = pd.read_excel('data_02_lab_quotas.xlsx')

#%%
"""Plot lab test referrals for 2 groups"""

#Some GP doctors exceed quotas for referrals for lab tests. 
#Compare 40 GP who exceed quotas with 40 GP who don't exceed quotas. 
#Plot lab test referrals for different lab test categories in 2020 per 1 registred patient for 2 GP groups. 

#%%
# group by specialist, lab test category
# for each lab test category calculate sum of manipulations in year 2020 (for each specialist) and 
# calculate manipulations per registred patient

data_specialist_manip_cat = (data>>
ply.group_by(ply.X.specialist_id, ply.X.manipulation_category, ply.X.quota_limit_exceeded, ply.X.number_of_patients) >>
ply.summarize(sum_manipulation = ply.X.sum_manipulation.sum()) >>
ply.mutate(manip_per_patient = ply.X.sum_manipulation/ply.X.number_of_patients))

#%%
# Plot
f, ax = plt.subplots(figsize = (10,10))
sns.despine(bottom=True, left=True)

g = sns.stripplot(x="manip_per_patient", y="manipulation_category", hue="quota_limit_exceeded",
              data=data_specialist_manip_cat, dodge=True, alpha=.25, zorder=1)

g = sns.pointplot(x="manip_per_patient", y="manipulation_category", hue="quota_limit_exceeded",
              data=data_specialist_manip_cat, dodge=.8 - .8 / 2,
              join=False, palette="dark",
              markers="d", scale=.75, ci=None)

ax.set_xlabel('Manipulations per 1 registred patient in 2020')
ax.set_ylabel('Lab test category')
ax.set_title('')

new_labels = ['quota exceeded', 'quota not exceeded', 'quota exceeded, average', 'quota not exceeded, average']

h, l = ax.get_legend_handles_labels()
ax.legend(h, new_labels, title="Labels")
plt.savefig('Lab_test_catogories_2_groups.png', dpi = 400, bbox_inches="tight")


# %%
"""Plot lab test category combinations in April 2020"""

# Do GP refer patient to one or more lab test categories in the same medical record?
# What are the most common combinations of lab test categories in referrals?
# Check medical records of April 2020.

#read data from excel
data2 = pd.read_excel('data_02_lab_test_combinations.xlsx')

# %%
# group by medical record ID and lab test category. 

data_MR_manip_cat = (data2 >>
ply.group_by(ply.X.specialist_id, ply.X.medical_record_id, ply.X.manipulation_category) >>
ply.summarize(sum_manipulation = ply.X.sum_manipulation.sum())
) #sum_manipulation is not signigicant value

# %%
# Boolean cross table for medical record and lab test category. 

data_cross = pd.crosstab(data_MR_manip_cat.medical_record_id, data_MR_manip_cat.manipulation_category).astype(bool)

# %%
# plot Upsetplot

from upsetplot import from_indicators, UpSet
from upsetplot import generate_counts, plot

data_upset = from_indicators(data_cross, data = data_cross) #make DataFrame ready for upsetplot. 
#more info in Upsetplot documentation

g = UpSet(data_upset, show_counts = True).plot() #plot
plt.savefig('manip_cat_combinations.png', dpi = 400, bbox_inches="tight") #save fugure

