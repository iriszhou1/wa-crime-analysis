"""
Katherine
CSE 163
This file includes a method to filter out the datasets of unemployment
rates and crime rates of each county from 2012 to 2020.

There's another method which uses the cleared datasets to plot five plots which
have eight subplots in each of them. The subplots depict how the unemployment
rates and crime occurrences change from 2012 to 2020 in those five counties
which are Benton, King, Yakima, Spokane, and Snohomish.
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set()

WA_CRIME_DATA = "data/washington_crime.csv"
UNEMPLOYMENT_PATH = "data/info_county/"


def filter_data(crime_data_wa, unemployment_file_path):
    """
    Takes the file path for unemployment information and crime dataset
    Get the "COUNTY TOTAL" crime data from the datasets for Washington State
    Access the 2020 unemployment rate information from different datasets by
    the given path
    """
    # crime data
    wa_crime_data = pd.read_csv(crime_data_wa)
    wa_crime_data_cleared = wa_crime_data[(wa_crime_data["LOCATION"]
                                           == "COUNTY TOTAL")]

    cleared_path = "data/cleared_datasets/crime_data_cleared.csv"
    wa_crime_data_cleared.to_csv(cleared_path)
    crime_data_cleared = pd.read_csv(cleared_path)

    # combine unemployment datasets
    file_list = []
    for f in os.listdir(unemployment_file_path):
        file_list.append(pd.read_csv(os.path.join(unemployment_file_path, f)))
    combined = pd.concat(file_list)
    combined = combined[(combined["County Name/State Abbreviation"].str[-2:]
                         == "WA")]
    combined = combined.sort_values(by='Year')

    cleared_unemployment_path = "data/cleared_datasets/unemployment_data.csv"
    combined.to_csv(cleared_unemployment_path)
    unemployment_data = pd.read_csv(cleared_unemployment_path)
    return [crime_data_cleared, unemployment_data]


def plot_correlation(dataset_list):
    crime_data_cleared = dataset_list[0]
    unemployment_data = dataset_list[1]
    # crime_rates_2020 = crime_data_cleared[(crime_data_cleared["INDEXYEAR"]
    #    == 2020)]
    # outliers
    # total across counties
    # crime_rates_2020 = crime_data_cleared[(crime_data_cleared["INDEXYEAR"]
    #                                        == 2020)]["RATE"]
    # unemployment_rates_2020 = unemployment_data[(unemployment_data["Year"]
    #                                            == 2020)]
    # crime_rates_2020 = crime_rates_2020.sort_values(by="RATE")
    # unemployment_rates_2020 = unemployment_rates_2020.sort_values()

    # plots
    years = np.array([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])

    # Benton
    benton_crime = crime_data_cleared[(crime_data_cleared["COUNTY"]
                                       == "BENTON")]
    benton_unemployment =\
        unemployment_data[(unemployment_data["County Name/State Abbreviation"]
                           == "Benton County, WA")]
    benton_crime_data = benton_crime["RATE"]
    benton_burglary_data = benton_crime["BURGLARY"]
    benton_theft_data = benton_crime["THEFT"]
    benton_drug_data = benton_crime["DRUG_VIOLATIONS"]
    benton_prostitution_data = benton_crime["PROSTITUTION"]
    benton_porn_data = benton_crime["PORNOGRAPHY"]
    benton_kid_data = benton_crime["KIDNAPPING_ABDUCTION"]
    benton_unemployment_data = benton_unemployment["Unemployment Rate"]

    y1 = benton_unemployment_data.to_numpy()
    y2 = benton_crime_data.to_numpy()
    y3 = benton_burglary_data.to_numpy()
    y4 = benton_theft_data.to_numpy()
    y5 = benton_drug_data.to_numpy()
    y6 = benton_prostitution_data.to_numpy()
    y7 = benton_porn_data.to_numpy()
    y8 = benton_kid_data.to_numpy()

    fig_b, ax = plt.subplots(4, 2, figsize=(6, 9))
    fig_b.suptitle('Unemployment and Crime - Benton')
    ax[0, 0].plot(years, y1, color='purple')
    ax[0, 0].set_title('Unemployment', loc='left', fontsize=8,
                       fontweight='bold')
    ax[0, 1].plot(years, y2)
    ax[0, 1].set_title('Total', loc='left', fontsize=8, fontweight='bold')
    ax[1, 0].plot(years, y3)
    ax[1, 0].set_title('Burglary', loc='left', fontsize=8, fontweight='bold')
    ax[1, 1].plot(years, y4)
    ax[1, 1].set_title('Theft', loc='left', fontsize=8, fontweight='bold')
    ax[2, 0].plot(years, y5)
    ax[2, 0].set_title('Drug', loc='left', fontsize=8, fontweight='bold')
    ax[2, 1].plot(years, y6)
    ax[2, 1].set_title('Prostitution', loc='left',
                       fontsize=8, fontweight='bold')
    ax[3, 0].plot(years, y7)
    ax[3, 0].set_title('Porn', loc='left', fontsize=8, fontweight='bold')
    ax[3, 1].plot(years, y8)
    ax[3, 1].set_title('Kidnapping', loc='left', fontsize=8, fontweight='bold')
    for x in range(4):
        for y in range(2):
            ax[x, y].tick_params('y', labelsize=8)
            ax[x, y].tick_params('x', labelsize=8)
    fig_b.tight_layout()
    fig_b.savefig('plots/unemployment/benton_plot.png')
    # fig_b.show()

    # Yakima
    yakima_crime = crime_data_cleared[(crime_data_cleared["COUNTY"]
                                       == "YAKIMA")]
    yakima_unemployment =\
        unemployment_data[(unemployment_data["County Name/State Abbreviation"]
                           == "Yakima County, WA")]
    ya_crime_data = yakima_crime["RATE"]
    ya_burglary_data = yakima_crime["BURGLARY"]
    ya_theft_data = yakima_crime["THEFT"]
    ya_drug_data = yakima_crime["DRUG_VIOLATIONS"]
    ya_prostitution_data = yakima_crime["PROSTITUTION"]
    ya_porn_data = yakima_crime["PORNOGRAPHY"]
    ya_kid_data = yakima_crime["KIDNAPPING_ABDUCTION"]
    ya_unemployment_data = yakima_unemployment["Unemployment Rate"]

    y1 = ya_unemployment_data.to_numpy()
    y2 = ya_crime_data.to_numpy()
    y3 = ya_burglary_data.to_numpy()
    y4 = ya_theft_data.to_numpy()
    y5 = ya_drug_data.to_numpy()
    y6 = ya_prostitution_data.to_numpy()
    y7 = ya_porn_data.to_numpy()
    y8 = ya_kid_data.to_numpy()

    fig_ya, ax = plt.subplots(4, 2, figsize=(6, 9))
    fig_ya.suptitle('Unemployment and Crime - Yakima')
    ax[0, 0].plot(years, y1, color='purple')
    ax[0, 0].set_title('Unemployment', loc='left',
                       fontsize=8, fontweight='bold')
    ax[0, 1].plot(years, y2)
    ax[0, 1].set_title('Total', loc='left', fontsize=8, fontweight='bold')
    ax[1, 0].plot(years, y3)
    ax[1, 0].set_title('Burglary', loc='left', fontsize=8, fontweight='bold')
    ax[1, 1].plot(years, y4)
    ax[1, 1].set_title('Theft', loc='left', fontsize=8, fontweight='bold')
    ax[2, 0].plot(years, y5)
    ax[2, 0].set_title('Drug', loc='left', fontsize=8, fontweight='bold')
    ax[2, 1].plot(years, y6)
    ax[2, 1].set_title('Prostitution', loc='left',
                       fontsize=8, fontweight='bold')
    ax[3, 0].plot(years, y7)
    ax[3, 0].set_title('Porn', loc='left', fontsize=8, fontweight='bold')
    ax[3, 1].plot(years, y8)
    ax[3, 1].set_title('Kidnapping', loc='left', fontsize=8, fontweight='bold')
    for x in range(4):
        for y in range(2):
            ax[x, y].tick_params('y', labelsize=8)
            ax[x, y].tick_params('x', labelsize=8)
    fig_ya.tight_layout()
    fig_ya.savefig('plots/unemployment/yakima_plot.png')
    # fig_ya.show()

    # Spokane
    spo_crime = crime_data_cleared[(crime_data_cleared["COUNTY"] == "SPOKANE")]
    spo_unemployment =\
        unemployment_data[(unemployment_data["County Name/State Abbreviation"]
                           == "Spokane County, WA")]
    spo_crime_data = spo_crime["RATE"]
    spo_burglary_data = spo_crime["BURGLARY"]
    spo_theft_data = spo_crime["THEFT"]
    spo_drug_data = spo_crime["DRUG_VIOLATIONS"]
    spo_prostitution_data = spo_crime["PROSTITUTION"]
    spo_porn_data = spo_crime["PORNOGRAPHY"]
    spo_kid_data = spo_crime["KIDNAPPING_ABDUCTION"]
    spo_unemployment_data = spo_unemployment["Unemployment Rate"]

    y1 = spo_unemployment_data.to_numpy()
    y2 = spo_crime_data.to_numpy()
    y3 = spo_burglary_data.to_numpy()
    y4 = spo_theft_data.to_numpy()
    y5 = spo_drug_data.to_numpy()
    y6 = spo_prostitution_data.to_numpy()
    y7 = spo_porn_data.to_numpy()
    y8 = spo_kid_data.to_numpy()

    fig_spo, ax = plt.subplots(4, 2, figsize=(6, 9))
    fig_spo.suptitle('Unemployment and Crime - Spokane')
    ax[0, 0].plot(years, y1, color='purple')
    ax[0, 0].set_title('Unemployment', loc='left',
                       fontsize=8, fontweight='bold')
    ax[0, 1].plot(years, y2)
    ax[0, 1].set_title('Total', loc='left', fontsize=8, fontweight='bold')
    ax[1, 0].plot(years, y3)
    ax[1, 0].set_title('Burglary', loc='left', fontsize=8, fontweight='bold')
    ax[1, 1].plot(years, y4)
    ax[1, 1].set_title('Theft', loc='left', fontsize=8, fontweight='bold')
    ax[2, 0].plot(years, y5)
    ax[2, 0].set_title('Drug', loc='left', fontsize=8, fontweight='bold')
    ax[2, 1].plot(years, y6)
    ax[2, 1].set_title('Prostitution', loc='left',
                       fontsize=8, fontweight='bold')
    ax[3, 0].plot(years, y7)
    ax[3, 0].set_title('Porn', loc='left', fontsize=8, fontweight='bold')
    ax[3, 1].plot(years, y8)
    ax[3, 1].set_title('Kidnapping', loc='left', fontsize=8, fontweight='bold')
    for x in range(4):
        for y in range(2):
            ax[x, y].tick_params('y', labelsize=8)
            ax[x, y].tick_params('x', labelsize=8)
    fig_spo.tight_layout()
    fig_spo.savefig('plots/unemployment/spokane_plot.png')
    # fig_spo.show()

    # King
    king_crime = crime_data_cleared[(crime_data_cleared["COUNTY"] == "KING")]
    king_unemployment =\
        unemployment_data[(unemployment_data["County Name/State Abbreviation"]
                           == "King County, WA")]
    king_crime_data = king_crime["RATE"]
    king_burglary_data = king_crime["BURGLARY"]
    king_theft_data = king_crime["THEFT"]
    king_drug_data = king_crime["DRUG_VIOLATIONS"]
    king_prostitution_data = king_crime["PROSTITUTION"]
    king_porn_data = king_crime["PORNOGRAPHY"]
    king_kid_data = king_crime["KIDNAPPING_ABDUCTION"]
    king_unemployment_data = king_unemployment["Unemployment Rate"]

    y1 = king_unemployment_data.to_numpy()
    y2 = king_crime_data.to_numpy()
    y3 = king_burglary_data.to_numpy()
    y4 = king_theft_data.to_numpy()
    y5 = king_drug_data.to_numpy()
    y6 = king_prostitution_data.to_numpy()
    y7 = king_porn_data.to_numpy()
    y8 = king_kid_data.to_numpy()

    fig_k, ax = plt.subplots(4, 2, figsize=(6, 9))
    fig_k.suptitle('Unemployment and Crime - King')
    ax[0, 0].plot(years, y1, color='purple')
    ax[0, 0].set_title('Unemployment', loc='left',
                       fontsize=8, fontweight='bold')
    ax[0, 1].plot(years, y2)
    ax[0, 1].set_title('Total', loc='left', fontsize=8, fontweight='bold')
    ax[1, 0].plot(years, y3)
    ax[1, 0].set_title('Burglary', loc='left', fontsize=8, fontweight='bold')
    ax[1, 1].plot(years, y4)
    ax[1, 1].set_title('Theft', loc='left', fontsize=8, fontweight='bold')
    ax[2, 0].plot(years, y5)
    ax[2, 0].set_title('Drug', loc='left', fontsize=8, fontweight='bold')
    ax[2, 1].plot(years, y6)
    ax[2, 1].set_title('Prostitution', loc='left',
                       fontsize=8, fontweight='bold')
    ax[3, 0].plot(years, y7)
    ax[3, 0].set_title('Porn', loc='left', fontsize=8, fontweight='bold')
    ax[3, 1].plot(years, y8)
    ax[3, 1].set_title('Kidnapping', loc='left', fontsize=8, fontweight='bold')
    for x in range(4):
        for y in range(2):
            ax[x, y].tick_params('y', labelsize=8)
            ax[x, y].tick_params('x', labelsize=8)
    fig_k.tight_layout()
    fig_k.savefig('plots/unemployment/king_plot.png')
    # fig_k.show()

    # Snohomish County
    sno_crime = crime_data_cleared[(crime_data_cleared["COUNTY"]
                                    == "SNOHOMISH")]
    sno_unemployment =\
        unemployment_data[(unemployment_data["County Name/State Abbreviation"]
                           == "Snohomish County, WA")]
    sno_crime_data = sno_crime["RATE"]
    sno_burglary_data = sno_crime["BURGLARY"]
    sno_theft_data = sno_crime["THEFT"]
    sno_drug_data = sno_crime["DRUG_VIOLATIONS"]
    sno_prostitution_data = sno_crime["PROSTITUTION"]
    sno_porn_data = sno_crime["PORNOGRAPHY"]
    sno_kid_data = sno_crime["KIDNAPPING_ABDUCTION"]
    sno_unemployment_data = sno_unemployment["Unemployment Rate"]

    y1 = sno_unemployment_data.to_numpy()
    y2 = sno_crime_data.to_numpy()
    y3 = sno_burglary_data.to_numpy()
    y4 = sno_theft_data.to_numpy()
    y5 = sno_drug_data.to_numpy()
    y6 = sno_prostitution_data.to_numpy()
    y7 = sno_porn_data.to_numpy()
    y8 = sno_kid_data.to_numpy()

    fig_sno, ax = plt.subplots(4, 2, figsize=(6, 9))
    fig_sno.suptitle('Unemployment and Crime - Snohomish')
    ax[0, 0].plot(years, y1, color='purple')
    ax[0, 0].set_title('Unemployment', loc='left',
                       fontsize=8, fontweight='bold')
    ax[0, 1].plot(years, y2)
    ax[0, 1].set_title('Total', loc='left', fontsize=8, fontweight='bold')
    ax[1, 0].plot(years, y3)
    ax[1, 0].set_title('Burglary', loc='left', fontsize=8, fontweight='bold')
    ax[1, 1].plot(years, y4)
    ax[1, 1].set_title('Theft', loc='left', fontsize=8, fontweight='bold')
    ax[2, 0].plot(years, y5)
    ax[2, 0].set_title('Drug', loc='left', fontsize=8, fontweight='bold')
    ax[2, 1].plot(years, y6)
    ax[2, 1].set_title('Prostitution', loc='left',
                       fontsize=8, fontweight='bold')
    ax[3, 0].plot(years, y7)
    ax[3, 0].set_title('Porn', loc='left', fontsize=8, fontweight='bold')
    ax[3, 1].plot(years, y8)
    ax[3, 1].set_title('Kidnapping', loc='left', fontsize=8, fontweight='bold')
    for x in range(4):
        for y in range(2):
            ax[x, y].tick_params('y', labelsize=8)
            ax[x, y].tick_params('x', labelsize=8)
    fig_sno.tight_layout()
    fig_sno.savefig('plots/unemployment/snohomish_plot.png')
    # fig_sno.show()


def main():
    dataset_list = filter_data(WA_CRIME_DATA, UNEMPLOYMENT_PATH)
    plot_correlation(dataset_list)


if __name__ == '__main__':
    main()
