Analyzing The Relationship Between Job Turnover And Gender Using NLS79
Data
================

### Anisha Grover

## Objective

The objective of this analysis is to look for patterns in job switching
behavior of the working age population and investigate if there are any
differences by gender. For this purpose the 1979 cohort of the National
Longitudinal Survey of Youth (NLSY79) has been used. The survey tracks
12686 men and women born in the United States during the years 1957-1964
over 28 rounds of survey creating a forty year long panel data.

## Directory Structure

    ├── readme.md
    ├── readme.txt
    ├── requirements.txt
    ├── data
    |   ├── interim
    |   └── processed
    ├── notebooks
    ├── reports
    └── scripts

- The *data/interim* folder contains data files which have been
  converted from the wide format available on the survey website, to the
  long format and labelled correctly. Details of the data in these files
  is described in *data/interim/data_description.txt*.
- The *data/processed* folder is where the script *gen_features.py*
  stores the cleaned data with features to be used in the analysis.
- The *notebooks* folder contains the jupyter notebook
  *job_switching_gender_analysis.ipynb* where the analysis is done.
- The *reports* folder contains a pdf version of the analysis done in
  the notebook.
- The *scripts* folder contains *gen_features.py* that takes data from
  the data/interim folder and creates two data frames with cleaned
  features that will be used in the analysis.

## Instructions for Running the Program

- Check if Python3 and pip are installed.
- Check if all modules in *requirements.txt* are installed.

### Running the analysis in Jupyter Notebook

- Ensure that JupyterLab is installed on your system. The instructions
  for installation can be found [here](https://jupyter.org/install).
- Using the command line, navigate to the python_sample/notebooks
  folder.
- Run the command
  `jupyter notebook job_switching_gender_analysis.ipynb`. This will open
  the notebook in a browser window.
- Click the menu *Cells* -\> *Run All*. This will first set the correct
  working directory, run the *gen_features.py* to create the data frames
  needed for the analysis and then run the data analysis.

### Viewing pdf of the analysis

- A pdf version of the analysis
  *300123_job_switching_gender_analysis.pdf* is stored in the *reports*
  folder.

### Running the script *gen_features.py* independently

- Navigate to the script and uncomment the code in the docstrings to
  automatically set the directory for running the code.
- Run `python3 gen_features.py` in the command line.

## Acknowledgements

This analysis was initiated as a part of a group project requirement
during the Correlation One Data Science For All Fellowship (July-Aug
2022). The idea for this analysis as well as the project code is my
individual work and i am responsible for all the errors. I would like to
thank my team members Danni Chen, Wenjing Dong, Yuan Du and Yifan Ma for
feedback.

## Disclaimer

The data used for the project was downloaded from the NLS Investigator
after registering an account with them and is subject to National
Longitudinal Survey Team's terms and conditions.

