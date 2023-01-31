#! python3
# gen_features.py - Merges data in 'data/interim' folder, generates new features from them and saves the features required for analysis to 'jobs_unique_data.csv' and 'jobs_switch_data.csv' in 'data/processed' folder.


# Import modules
import pandas as pd
import numpy as np
from pathlib import Path
import os


# Uncomment and use only if running this script independently
"""
path_to_this_file = Path(os.path.dirname(__file__))
project_dir_path = path_to_this_file.parents[0]
os.chdir(project_dir_path)
"""


# Read files from 'data/interim' folder
data_folder    = Path('./data/interim')
jobs_df        = pd.read_csv(data_folder/Path('jobs_data.csv'))
gender_df      = pd.read_csv(data_folder/Path('gender_data.csv'))
education_df   = pd.read_csv(data_folder/Path('highest_grade_completed_data.csv')) 
job_type_df    = pd.read_csv(data_folder/Path('job_type_data.csv'))
job_history_df = pd.read_csv(data_folder/Path('job_history_data.csv'))
age_df         = pd.read_csv(data_folder/Path('age_data.csv'))

########################################################################################

# Create column 'Years_Job_History' in jobs_data that counts the number of years a person is seen in the employment data

jobs_df['Years_Job_History'] = (jobs_df
                                   .groupby('Person_Id')['Person_Id']
                                   .transform('count'))


# Create new dataframe jobs_unique_df from jobs_df by keeping only one row per respondent and selecting columns Person_Id, Total_Jobs and Years_Job_History that do not vary with years
jobs_unique_df = (jobs_df[['Person_Id','Total_Jobs','Years_Job_History']]
                     .drop_duplicates())


########################################################################################

# Create features related to gender and merge with jobs_unique_df

# Create column 'Female' that is 1 if gender is female.
gender_df['Female'] = np.where(gender_df['Gender'] == 1, 0, 1)

# Create column 'Gender_Level' with labels 'Male' and 'Female.
gender_df['Gender'] = np.where(gender_df['Female'] == 0, 'Male', 'Female')

# Select relevant columns from gender_df and merge with jobs_unique_df
gender_df = gender_df[['Person_Id', 'Female', 'Gender']]

jobs_unique_df = jobs_unique_df.merge(gender_df, on = 'Person_Id', how = 'left')


########################################################################################

# Create features related to education and merge with jobs_unique_df

# Create Education_Ctg column that converts numeric maximum years of education to four categories
education_conditions = [
    (education_df['Max_Education'] < 12),
    ((education_df['Max_Education'] >= 12) & (education_df['Max_Education'] <= 14)),
    ((education_df['Max_Education'] >= 15) & (education_df['Max_Education'] <= 16)),
    (education_df['Max_Education'] >= 17)
     ]

education_labels = ['Less_School', 'Complete_School', 'College', 'Graduate']

education_df['Education_Ctg'] = np.select(education_conditions, education_labels)

# Select relevant columns from education_df and merge with unique_jobs_df
education_df = education_df[['Person_Id', 'Education_Ctg']]

jobs_unique_df = (jobs_unique_df
                     .merge(education_df, on = ['Person_Id'], how = 'left'))

########################################################################################

# Create features that track the fraction of years employed in different job categories from column Job_Type and merge with jobs_unique_df

# Merge column Job_Type to the job_history_df (as job type varies with job)
# Since a single job can have multiple job types (for e.g. due to a person skipping the question in one year), i will keep only the max Job_Type for a job to ensure uniqueness and then merge

# Keep unique 'Job_Type' code for each job by taking a max.
job_type_df = (job_type_df
                  .groupby(['Person_Id', 'Job_ID'])
                  .agg(Job_Type = ('Job_Type', 'max'))
                  .reset_index())
            


# Merge Job_Type column with job_history_df
job_history_df = (job_history_df
                     .set_index(['Person_Id', 'Job_ID'])
                     .join(job_type_df.set_index(['Person_Id', 'Job_ID']), how = 'left')
                     .reset_index())


# Create column Job_Ctg that converts numeric column Job_Type to 3 categories 
job_history_df['Job_Ctg'] = np.where(((job_history_df['Job_Type'] == 1) | 
                                    (job_history_df['Job_Type'] == 5)),
                               'Pvt', 
                                np.where(job_history_df['Job_Type'] == 2, 'Gvt',
                                    'Other'))                                     
                                   

# Create new job_ctg_df that counts the number of years worked in each job category for  each respondent

job_ctg_df = pd.get_dummies(
                 job_history_df[['Person_Id', 'Calendar_Year', 'Job_ID', 'Job_Ctg']], 
                 columns = ['Job_Ctg']
                 )


job_ctg_df = (job_ctg_df[['Person_Id', 'Calendar_Year', 'Job_Ctg_Gvt',      
                     'Job_Ctg_Pvt','Job_Ctg_Other']]
                .drop_duplicates()
                .groupby(['Person_Id'])
                .agg(Years_Job_History = ('Calendar_Year', 'nunique'),
                    Years_Gvt_Job = ('Job_Ctg_Gvt', 'sum'),
                    Years_Pvt_Job = ('Job_Ctg_Pvt', 'sum'),
                    Years_Self_Job = ('Job_Ctg_Other', 'sum')))


# Create 3 columns that calculate the fraction of working years spent in each job category for each respondent
job_ctg_df['Frac_Years_Pvt']  = round(100 * (job_ctg_df['Years_Pvt_Job'] /
                                             job_ctg_df['Years_Job_History']))
                                    
job_ctg_df['Frac_Years_Gvt']  = round(100 * (job_ctg_df['Years_Gvt_Job'] / 
                                             job_ctg_df['Years_Job_History']))
                                      
job_ctg_df['Frac_Years_Self'] = round(100 * (job_ctg_df['Years_Self_Job'] /
                                             job_ctg_df['Years_Job_History']))


# Select relevant columns from job_ctg_df and merge with jobs_unique_df
job_ctg_df = (job_ctg_df
                 .reset_index()[['Person_Id', 'Frac_Years_Pvt', 'Frac_Years_Gvt',  
                                 'Frac_Years_Self']])      

jobs_unique_df = jobs_unique_df.merge(job_ctg_df, on = 'Person_Id', how = 'left')

########################################################################################

# Create jobs_switch_df that selects columns from jobs_df needed for analysis of job switching behaviour and merges them with age_df

jobs_switch_df = (jobs_df[['Person_Id', 'Calendar_Year', 'Switch_Job_1', 'Switch_Job_2']]
                    .merge(age_df, on = ['Person_Id', 'Calendar_Year'], how = 'left'))

# Reorder columns
jobs_switch_df = jobs_switch_df[['Person_Id', 'Calendar_Year', 'Age', 'Switch_Job_1', 
                                 'Switch_Job_2']]

########################################################################################


# Save jobs_unique_df and jobs_switch_df to 'data/processed'
# If a file already exists, it is overwritten.

jobs_unique_df.to_csv('./data/processed/jobs_unique_data.csv')
jobs_switch_df.to_csv('./data/processed/jobs_switch_data.csv')

print('Processed data files saved.')

########################################################################################