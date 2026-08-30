# **Course project:** Implicit gender bias in language processing

**Authors:** *Aylina Ashkenov*, *Qianyue Li*, *Sakshi Takawale*, *Sophie Schüttler*

**Course:** *Acquisition and analysis of eye-tracking data*

**Semester:** *Summer semester 2026*

## Project Description

> The main goal of the experiment is to find out whether different forms of German role nouns (masculine, feminine, gender-inclusive) elict a gender bias. Eye-tracking is used in this project to examine the reading behaviour while reading differnt role noun forms with male or female anaphor refering to that role noun. To measure their reading behaviour on the role noun and anaphor measures such as fixation times, go past time and regressions is used. In detail the project investigates whether the male roule noun creates a stronger male bias, femine role noun creates a female bias and whether the gender-inclusive star form creates no bias.

## Experiment Instruction

> To perform the experiment, first open the OpenSesame file experiment.osexp. It's important to ensure that the experiment is using PsychoPy as backend. The exeriment has set the screen resolution of 1920 x 1080 pixels. If the used screen has a different resolution either change the screen resolution or the setting in the OpenSesame experiment. In addition the experimental list must be selected in "liste_auswahl" depending on the participants subject number. This is important so each participant is presented with the correct list according to the latin-square design.

## Data Analysis Instruction

> Packages needed: [eyekit](https://github.com/jwcarr/eyekit), [cateyes](https://doi.org/10.5281/zenodo.21914293), [I2MC](https://github.com/dcnieho/I2MC_Python), [lmerTest (R)](https://github.com/runehaubo/lmerTestR)
>
> *For the specifics on the usage of each script (input, output, note of usage) listed below, see the corresponding files.*
>
> **Step00. Text layout reconstruction:**
>
> -   Run: `python -m src.text_processing`
>
> -   Purpose: split the text into separate lines for later usage of text alignment in eyekit (Step03).
>
> **Step01. Cleaning**
>
> -   Run: `python -m scripts.01_clean`
>
> -   Purpose: validity filtering; unit conversion
>
> -   Inspection -\> `plots/quality_control/01_clean/`; `stats/01_clean/`
>
> **Step02. Fixation detection**
>
> -   Run: `python -m scripts.02_fixation_detection`
>
> -   Purpose: fixation detection using I-VT (quality control only), I-DT (quality control only), I2MC; merge/duration filter; tail truncation
>
> -   Inspection -\> `plots/quality_control/02_fixation/`
>
> **Step03. Drift correction**
>
> -   Run: `python -m scripts.03_drift_correction`
>
> -   Purpose: eyekit line snapping (chain/regress/cluster ensemble); (step 0's text layout is used here)
>
> -   Inspection -\> `plots/quality_control/03_drift/`; `stats/03_drift/`
>
> **Step04. Analysis**
>
> -   Run: `python -m scripts.04_analysis --balanced`
>
> -   Purpose: AOI measures (initial fixation duration, go-past duration, regression-in counts, total fixation duration)
>
> -   Inspection -\> `data/processed/balanced_12/analysis_results.csv`
>
> **Step05. Statistics**
>
> -   *Note: original analysis was done without pbkrtest package, so used Satterthwaite approximation as fallback instead.*
>
> -   Run: `Rscript scripts/stats_lmm.R`
>
> -   Purpose: fit linear mixed-effects model for role noun forms and anaphor genders, and their interaction
>
> -   Inspection -\> `data/stats/analysis/analysis_stats.txt`
>
> -   Run: `Rscript scripts/stats_correlation.R`
>
> -   Purpose: correlation analysis for measure results and questionnaire responses
>
> -   Inspection -\> `data/stats/analysis/analysis_stats.txt`; `plots/analysis/balanced_12/stats/`
>
> **Further quality checks** (need to complete Step01 first)
>
> -   Run: `python -m scripts.qc_events`
>
> -   Purpose: plot for events across time
>
> -   Inspection -\> `plots/quality_control/qc_events/`
>
> -   Run: `python -m scripts.qc_acc_prec`
>
> -   Purpose: plot accuracy and precision on the fixation cross across trials
>
> -   Inspection -\> `plots/quality_control/qc_acc_prec/`
>
> **Other:**
>
> -   after running the preprocessing steps, can go to notebooks/pipeline_inspection.ipynb to play around with interactive gaze path, different drift correction methods, etc.

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
├── plots              <- All exported plots go here
|   ├── alignment      <- sanity check of the text alingment from experiment screenshots
|   ├── analysis       <- Plotting from measurement analysis, questionniare analysis, statistics
|   ├── quality_control<- Plotting to ensure the data quality
|       ├── 01_clean   <- Gaze across time before and after cleaning
|       ├── 02_fixation<- Gaze classificaiton, fixation distribution, main sequence
|       ├── 03_drift   <- Gaze-path before and after drift correction
|       ├── qc_acc_prec<- Accuracy and Precision plotting
|       ├── qc_events  <- Events across time
│
├── scripts            <- Various scripts, e.g. analysis and plotting.
│                         The scripts use the `src` folder for their base code.
│                         
│
├── src                <- Source code for use in this project. Contains functions,
│                         structures and modules that are used throughout
│                         the project and in multiple scripts.
│
├── experiment         <- OpenSesame file to run the experiment; where applicable also stimuli, randomization
|
├── data               <- **If they have a reasonable file size**
|   ├── raw            <- Raw eye-tracking data
|   ├── interim        <- Data resulting from preprocessing
|   ├── assets         <- Font used for text-gaze overlay
|   ├── coding         <- Manually coded data used in processing
|   ├── processed      <- Final results from eyetracking measures
|   ├── questionnaire  <- Filled out quesionnaires and tables organizing the results
|   ├── stats          <- Stats during preprocessing steps; and the results from the final statistical analysis
| 
├── notebooks          <- jupyter notebooks to plot data for visualization for presentation and report 
|
├── config.py          <- config file containing all the parameters used in the analysis 
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

If your data is \<1GB you can add it to the data folder in your Git repository. Otherwise, only include it in the project package that you submit on Ilias at the end of the term.