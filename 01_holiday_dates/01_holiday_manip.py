
#%%
import pandas as pd
import numpy as np
import dfply as ply

#%%
"""Number of holidays and weekends within a time period of medical record"""

# manipulations used in medical records in this data can be used only during holidays or weekends.
# There is no information about date of manipulation, only start and end dates of medical record are known.

# This code checks, how many holidays or weekends are within time period of medical record.
# If 0, medical record has only working days, so doctor used manipulation in the wrong day.

#%%
# read data from excel
data = pd.read_excel('data_01_holiday_manipulations.xlsx')

# convert dates to datetime format
data['medical_record_start_date'] = pd.to_datetime(data['medical_record_start_date'], format="%Y.%m.%d")
data['medical_record_end_date'] = pd.to_datetime(data['medical_record_end_date'], format="%Y.%m.%d")

#%%
# import list of holiday and weekend dates from Jan 2021 to May 2022, convert to list
holiday_dates = pd.read_excel('holiday_dates.xlsx')
holiday_dates_list = holiday_dates['date'].tolist()

#%%
#calculate value, how many holidays or weekends are within time period of medical record
data['holiday_value'] = 0 

# for each holiday date in list, checks if this date is within medical record,
# if yes - adds +1. 
for i in range(len(holiday_dates_list)):
    data['holiday_value'] = np.where((data['medical_record_start_date']<=holiday_dates_list[i]) & 
    (data['medical_record_end_date']>=holiday_dates_list[i]), data['holiday_value']+1, data['holiday_value']+0)


#%%
#filter only medical records with 0 holidays or weekends. 
data_no_holidays = data[data.holiday_value==0]

#%%
# export data
temp = pd.ExcelWriter('output_01_holiday_manipulations.xlsx')
data.to_excel(temp, sheet_name='data')
data_no_holidays.to_excel(temp, sheet_name='data_no_holidays')
temp.save()
# %%
