# Analyzing Crime in Washington
**Authors:** Caroline Ding, Katherine Liu, Iris Zhou \
**Date:** June 6th, 2022

## Libraries Used:
* `numpy`
* `seaborn`
* `pandas`
* `geopandas`
* `matplotlib.pyplot`
* `plotly`
    + If you do not already have `plotly` installed, run `pip install plotly==5.8.0` or `conda install -c plotly plotly=5.8.0 ` from your terminal in VSCode after opening the project folder. 

## What to run:
* To run analysis and generate visualizations:
    + `src/crime_types.py`
    + `src/pop_density.py`
    + `src/unemployment.py`
* To test analysis files:
    + `src/crime_types_test.py`
    + `src/pop_density_test.py`

## Project Structure:
* `data`
    + Contains all data used for analysis.
* `plots`
    + Where plots generated in analysis files will be outputed.
* `src`
    + Contains all code for cleaning data, analyzing data, testing functions, and generating visualizations.
    + (test) `crime_types_test.py`
        - Tests methods from the module `crime_types.py`. Running the main method will run the tests using `assert_equals` statements (so no output will be produced if all the tests pass).
    + **[RUN]** `crime_types.py`
        - Running the main method will generate visuzalizations used for analysis. Interactive visualizations created using `plotly` will be opened in a web browser (17 visualizations total). 
    + `cse163_utils.py`
        - Contains `assert_equals` function used for testing.
    + (test) `pop_density_test.py`
        - Tests methods from the module `pop_density.py`. Running the main method will run the tests, produce a test plot saved to the `plots/pop/` folder, and open a test visualization in a web browser.
    + **[RUN]** `pop_density.py`
        - Running the main method will generate the visualizations and save any static plots in the folder named `plots/pop/`. Interactive visualziations created using `plotly` will be opened in a web browser.
    + **[RUN]** `unemployment.py`
        - Running the main method will run analysis on unemployment data, and outputs plots to the folder `plots/unemployment/`.
* Analyzing Crime in Washington **[PROJECT REPORT]**
* `README.md` (you are here)