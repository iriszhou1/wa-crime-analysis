# Analyzing Factors Related to Crime Rates in Washington State Counties
**Authors:** Iris Zhou, Katherine Liu, Caroline Ding

This project focused on factors contributing to changes in the crime rate in Washington state counties. Our analysis focused on three areas of interest: types of offenses reported, unemployment rate, and population density. We analyzed how each of these factors relate to location and crime rates.

 Looking at how the types of crime, unemployment rate, and population density relate to crime rates in different counties can help find what factors lead to higher crime rates. Knowing more about these factors can help inform specific measures and policy changes to improve safety for residents and change the underlying factors leading to criminal offenses.

The full project report can be viewed [here](https://iriszhou1.github.io/wa-crime-analysis/).

## Libraries Used:
* `numpy`
* `seaborn`
* `pandas`
* `geopandas`
* `matplotlib.pyplot`
* `plotly`
    + If you do not already have `plotly` installed, run `pip install plotly==5.8.0` or `conda install -c plotly plotly=5.8.0 ` from your terminal in VSCode after opening the project folder.
* `chart_studio`

## What to run:
* To run analysis and generate visualizations:
    + `src/crime_types.py`
    + `src/pop_density.py`
    + `src/unemployment.py`
* To test analysis files:
    + `src/crime_types_test.py`
    + `src/pop_density_test.py`

## Project Structure:
* `data`: Contains all data used for analysis.
* `plots`: Where plots generated in analysis files will be outputed. Also stores html pages for interative plots.
* `src`: Contains all code for cleaning data, analyzing data, testing functions, and generating visualizations.
    + **`crime_types_test.py`**: Tests methods from the module `crime_types.py`. Running the main method will run the tests using `assert_equals` statements (no output will be produced if all the tests pass).
    + **`crime_types.py`**: Running the main method will generate visuzalizations used for analysis. Interactive visualizations created using `plotly` can be opened in a web browser.
    + **`cse163_utils.py`**: Contains `assert_equals` function used for testing.
    + **`pop_density_test.py`**: Tests methods from the module `pop_density.py`. Running the main method will run the tests, produce a test plot saved to the `plots/pop/` folder, and open a test visualization in a web browser.
    + **`pop_density.py`**: Running the main method will generate the visualizations and save any static plots in the folder named `plots/pop/`. Interactive visualziations created using `plotly` will be opened in a web browser.
    + **`unemployment.py`**: Running the main method will run analysis on unemployment data, and outputs plots to the folder `plots/unemployment/`.
* `README.md` (you are here)
* `index.html`: Full report for analysis with plots embedded.
* `main.css`: Style for `index.html`.