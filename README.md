# **Course project:** Implicit gender bias in language processing
**Authors:** *Aylina Ashkenov*, *Qianyue Li*, *Sakshi Takawale*, *Sophie Schüttler* 

**Course:** *Acquisition and analysis of eye-tracking data*

**Semester:** *Summer semester 2026*

## Project Description
> The main goal of the experiment is to find out whether different forms of German role nouns (masculine, feminine, gender-inclusive) elict a gender bias. Eye-tracking is used in this project to examine the reading behaviour while reading differnt role noun forms with male or female anaphor refering to that role noun. To measure their reading behaviour on the role noun and anaphor measures such as fixation times, go past time and regressions is used. In detail the project investigates whether the male roule noun creates a stronger male bias, femine role noun creates a female bias and whether the gender-inclusive star form creates no bias.

## Experiment Instruction
> 

## Data Analysis Instruction
> @ Qianyue
> write here in what order you have to run your data to reproduce the results
>  What scripts, in which order, with which data need to be run?
>Be as specific as possible.
>
>Optional: Add a pipeline plot in which the different steps are displayed together with the corresponding scripts.

## Overview of Folder Structure 

```
│projectdir            <- Project's main folder. It is initialized as a Git
│                       repository with a reasonable .gitignore file.
│
├── report             <- Report PDF
|
├── presentation       <- Final presentation slides (PDF and .pptx)
|
├── _research          <- WIP scripts for data collection in lab, latin square design matrix as excel
│              
│
├── plots              <- All exported plots go here, best in date folders. Note that to ensure reproducibility it is required that all plots can be recreated using the plotting scripts in the scripts folder.
|   ├── alignment      <- alignment of the texts shown in experiment
|   ├── analysis       <- measurement analysis
|   ├── quality_control<- analysis to ensure the data quality
|       ├── 01_clean   <- data after preprocessing
|       ├── 02_fixation<- data
|       ├── 03_drift   <- data after drift correction
│
├── scripts            <- Various scripts, e.g. analysis and plotting.
│                         The scripts use the `src` folder for their base code.
│
├── src                <- Source code for use in this project. Contains functions,
│                         structures and modules that are used throughout
│                         the project and in multiple scripts.
│
├── experiment         <- OpenSesame file to run the experiment; where applicable also stimuli, randomization
|
├── data               <- **If they have a reasonable file size**
|   ├── raw            <- Raw eye-tracking data
|   ├── preprocessed   <- Data resulting from preprocessing
| 
├── notebooks          <- jupyter notebooks to plot data for visualization for presentation and report 
|
├── README.md          <- Top-level README. Fellow students need to be able to
|                         reproduce your project. Think about them!
|
├── .gitignore         <- List of files that you don’t want Git to automatically add
|                         (default Python .gitignore was used)
│
└── (requirements.txt)<- List of modules and packages that are used for your project
                     
```
## Note on sharing your recorded data
If your data is <1GB you can add it to the data folder in your Git repository. Otherwise, only include it in the project package that you submit on Ilias at the end of the term.
