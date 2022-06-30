"""
Caroline Ding
CSE 163
This is a file that includes the implementations for changing the shape of
DataFrame and merging two DataFrames by applying pandas. This file also
includes methods to plot interactive graphs, line graphs, and bar graphs.
"""


import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import chart_studio
import chart_studio.plotly as py

sns.set()


def select_pop_df(lst_column_names_pop, pop_df):
    """
    Given a population density dataframe. Returns a selected population density
    dataframe with county names(in upper case) and all the columns names in the
    list of column names.
    """
    select_pop_df = pop_df.loc[:, lst_column_names_pop]
    select_pop_df['COUNTY_NAME'] = select_pop_df['COUNTY_NAME'].str.upper()
    return select_pop_df


def change_pop_df_shape(lst_column_names_pop, select_pop_df):
    """
    Given a selected population density dataframe. Returns this dataframe in
    a new dataframe shape with 3 columns, county name, year, and population
    density. County names and years are sorted in ascending order.
    """
    new_select_pop_df = pd.melt(select_pop_df, id_vars=['COUNTY_NAME'],
                                value_vars=lst_column_names_pop[1:],
                                var_name='YEAR', value_name='POPDEN')

    new_select_pop_df = new_select_pop_df.sort_values(['COUNTY_NAME', 'YEAR'],
                                                      ascending=[True, True])
    new_select_pop_df['YEAR'] = \
        new_select_pop_df['YEAR'].str.replace('POPDEN_', '')
    # rearrange the index
    new_select_pop_df = new_select_pop_df.reset_index(drop=True)
    return new_select_pop_df


def select_crime_df(crime_df):
    """
    Given a crime rate dataframe. Returns a selected crime rate dataframe with
    county names, index year(in string), location(county total), and crime
    rate.
    """
    crime_df = crime_df.loc[:, ['COUNTY', 'INDEXYEAR', 'LOCATION', 'RATE']]
    county_total = crime_df['LOCATION'] == 'COUNTY TOTAL'
    select_crime_df = crime_df[county_total]
    select_crime_df = \
        select_crime_df.astype({"INDEXYEAR": str}, errors='raise')
    # rearrange the index
    select_crime_df = select_crime_df.reset_index(drop=True)
    return select_crime_df


def merge_pop_crime_df(new_select_pop_df, select_crime_df):
    """
    Given two selected dataframes in the same dataframe shape. Returns a merged
    dataframe according to the same county name and index year.
    """
    merged_df = new_select_pop_df.merge(select_crime_df, how='inner',
                                        left_on=['COUNTY_NAME', 'YEAR'],
                                        right_on=['COUNTY', 'INDEXYEAR'])
    return merged_df


def county_pop_greater_100(merged_df):
    """
    Given a merged dataframe. Returns a list of county names with population
    density greater than 100 in 2020.
    """
    year2020 = merged_df['YEAR'] == '2020'
    above100_pop = merged_df['POPDEN'] > 100
    new_merged_df = merged_df[year2020 & above100_pop]
    lst_county_names = list(new_merged_df['COUNTY_NAME'].values)
    return lst_county_names


def scattar_plot_df(merged_df, lst_county_names):
    """
    Given a merges dataframe and a list of county names that has population
    density greater then 100. Returns a dataframe used in scattar plot which
    contains only the counnties in the list of county names.
    """
    scatter_plot_df = \
        merged_df[merged_df['COUNTY_NAME'].isin(lst_county_names)]
    # rearrange the index
    scatter_plot_df = scatter_plot_df.reset_index(drop=True)
    return scatter_plot_df


def line_plot_pop_king_pierce(merged_df):
    """
    Given the merged dataframe. Returns two line charts that show the
    changes of poopulation density from 2012 to 2020 in King county and
    Pierce county.
    """
    select_king = merged_df['COUNTY_NAME'] == 'KING'
    select_pierce = merged_df['COUNTY_NAME'] == 'PIERCE'
    king_pierce_df = merged_df[select_king | select_pierce]
    sns.set(font_scale=0.7)
    plot = sns.relplot(data=king_pierce_df, x="YEAR", y="POPDEN", kind="line",
                       col="COUNTY_NAME", height=2, aspect=1)
    for ax in plot.axes.flat:
        labels = [2012 + i if i % 2 == 0 else '' for i in range(0, 9)]
        ax.set_xticklabels(labels, rotation=45)
    plt.xlabel('Year')
    plt.ylabel('Population Density')
    plt.savefig('plots/pop/line_plot_pop_king_pierce.png', bbox_inches='tight')
    sns.set(font_scale=1)


def line_plot_crime_king_pierce(merged_df):
    """
    Given the merged dataframe. Returns two line charts of that show the
    changes of crime rate  from 2012 to 2020 in King county and Pierce county.
    """
    select_king = merged_df['COUNTY_NAME'] == 'KING'
    select_pierce = merged_df['COUNTY_NAME'] == 'PIERCE'
    king_pierce_df = merged_df[select_king | select_pierce]
    sns.set(font_scale=0.7)
    plot = sns.relplot(data=king_pierce_df, x="YEAR", y="RATE", kind="line",
                       col="COUNTY_NAME", height=2, aspect=1)
    for ax in plot.axes.flat:
        labels = [2012 + i if i % 2 == 0 else '' for i in range(0, 9)]
        ax.set_xticklabels(labels, rotation=45)
    plt.xlabel('Year')
    plt.ylabel('Crime Rate per 1,000 Residents')
    plt.savefig('plots/pop/line_plot_crime_king_pierce.png',
                bbox_inches='tight')
    sns.set(font_scale=1)


def top4_pop_county_crime_df(lst_county_names_bar, crime_df):
    """
    Given the crime dataframe in washington and a list of county names.
    Returns a new dataframe with the counties in the given list county names
    and the crime rate for each crime type in year 2020.
    """
    crime_df2 = crime_df.astype({"INDEXYEAR": str}, errors='raise')
    year2020 = crime_df2['INDEXYEAR'] == '2020'
    choose_location = crime_df2['LOCATION'] == 'COUNTY TOTAL'
    crime_df2 = crime_df2[year2020 & choose_location]

    choose_4county_df = \
        crime_df2[crime_df2['COUNTY'].isin(lst_county_names_bar)]

    # delete the columns not relate to the crime types
    update_crime_df2 = choose_4county_df.drop(['INDEXYEAR', 'LOCATION',
                                               'POPULATION', 'TOTAL', 'RATE',
                                               'PRSNTOTAL', 'PRSNRATE',
                                               'PRPRTYTOTAL', 'PRPRTYRATE'],
                                              axis=1)
    return update_crime_df2


def new_shape_crime_df(update_crime_df2):
    """
    Given a dataframe. Returns this dataframe into a new shaped dataframe with
    three columns(county names, valiables, values) and all values are non-zero.
    """
    new_crime_df = pd.melt(update_crime_df2, id_vars=['COUNTY'])
    new_crime_df2 = new_crime_df[(new_crime_df[['value']] != 0).all(axis=1)]
    return new_crime_df2


def bar_plot_king_crime(new_crime_df2):
    """
    Given a dataframe. Returns a bar plot which shows the 5 highest count crime
    types in king county.
    """
    king_crime_df = new_crime_df2.loc[new_crime_df2.COUNTY == 'KING']
    king_crime_df2 = king_crime_df.nlargest(n=5, columns=['value'], keep='all')
    sns.catplot(x="value", y="variable", data=king_crime_df2, kind="bar",
                palette="Purples_r", height=4, aspect=1.8)
    plt.xlabel('Crime Count')
    plt.ylabel('Crime Types')
    plt.title('King County')
    plt.savefig('plots/pop/bar_plot_king_crime.png', bbox_inches='tight')


def bar_plot_clark_crime(new_crime_df2):
    """
    Given a dataframe. Returns a bar plot which shows the 5 highest count crime
    types in clark county.
    """
    clark_crime_df = new_crime_df2.loc[new_crime_df2.COUNTY == 'CLARK']
    clark_crime_df2 = \
        clark_crime_df.nlargest(n=5, columns=['value'], keep='all')
    sns.catplot(x="value", y="variable", data=clark_crime_df2, kind="bar",
                palette="Oranges_r", height=4, aspect=1.8)
    plt.xlabel('Crime Count')
    plt.ylabel('Crime Types')
    plt.title('Clark County')
    plt.savefig('plots/pop/bar_plot_clark_crime.png', bbox_inches='tight')


def bar_plot_kitsap_crime(new_crime_df2):
    """
    Given a dataframe. Returns a bar plot which shows the 5 highest count crime
    types in kitsap county.
    """
    kitsap_crime_df = new_crime_df2.loc[new_crime_df2.COUNTY == 'KITSAP']
    kitsap_crime_df2 = \
        kitsap_crime_df.nlargest(n=5, columns=['value'], keep='all')
    sns.catplot(x="value", y="variable", data=kitsap_crime_df2, kind="bar",
                palette="Blues_r", height=4, aspect=1.8)
    plt.xlabel('Crime Count')
    plt.ylabel('Crime Types')
    plt.title('Kitsap County')
    plt.savefig('plots/pop/bar_plot_kitsap_crime.png', bbox_inches='tight')


def bar_plot_pierce_crime(new_crime_df2):
    """
    Given a dataframe. Returns a bar plot which shows the 5 highest count crime
    types in pierce county.
    """
    pierce_crime_df = new_crime_df2.loc[new_crime_df2.COUNTY == 'PIERCE']
    pierce_crime_df2 = \
        pierce_crime_df.nlargest(n=5, columns=['value'], keep='all')
    sns.catplot(x="value", y="variable", data=pierce_crime_df2, kind="bar",
                palette="Greens_r", height=4, aspect=1.8)
    plt.xlabel('Crime Count')
    plt.ylabel('Crime Types')
    plt.title('Pierce County')
    plt.savefig('plots/pop/bar_plot_pierc_crime.png', bbox_inches='tight')


def main():
    # load two csv files
    POPULATION_FILE = "data/Population.csv"
    pop_df = pd.read_csv(POPULATION_FILE)
    CRIME_FILE = "data/wa_crime_report.csv"
    crime_df = pd.read_csv(CRIME_FILE)

    # list of columns that we are going to use in scatter plot and line plots
    lst_column_names_pop = ['COUNTY_NAME', 'POPDEN_2012', 'POPDEN_2013',
                            'POPDEN_2014', 'POPDEN_2015', 'POPDEN_2016',
                            'POPDEN_2017', 'POPDEN_2018', 'POPDEN_2019',
                            'POPDEN_2020']

    get_select_pop_df = select_pop_df(lst_column_names_pop, pop_df)
    update_select_pop_df = change_pop_df_shape(lst_column_names_pop,
                                               get_select_pop_df)

    get_select_crime_df = select_crime_df(crime_df)

    # merge two dataframes
    merged_df = merge_pop_crime_df(update_select_pop_df, get_select_crime_df)

    lst_county_names = county_pop_greater_100(merged_df)

    get_scatter_plot_df = scattar_plot_df(merged_df, lst_county_names)

    # Create a scattarplot which shows the relationship between population
    # density and crime rate from 2012 to 2020 in the counties with population
    # density greater than 100 in 2020.
    fig1 = px.scatter(get_scatter_plot_df, x="POPDEN", y="RATE",
                      color="COUNTY_NAME", trendline="ols",
                      trendline_scope="overall",
                      trendline_color_override="black",
                      width=800, height=500,
                      labels={"POPDEN": "Population Density (person per "
                              "square mile)",
                              "RATE": "Crime Rate per 1,000 Residents",
                              "COUNTY_NAME": "County names"},
                      title="Relationship Between Population Density and "
                            "Crime Rate in Counties<br>with Population "
                            "Density Greater than 100")
    fig1.show()

    # save plots to plotly account
    chart_studio.tools.set_credentials_file(username='irisz1',
                                            api_key='KpywulqM2TABw3Yt5hRo')
    py.plot(fig1, filename='pop_den_vs_crime_rate', auto_open=False)

    # two line plots
    line_plot_pop_king_pierce(merged_df)
    line_plot_crime_king_pierce(merged_df)

    # list of county names that we are going to use in bar plots
    lst_county_names_bar = ['KING', 'CLARK', 'KITSAP', 'PIERCE']
    update_crime_df2 = top4_pop_county_crime_df(lst_county_names_bar, crime_df)
    new_crime_df2 = new_shape_crime_df(update_crime_df2)

    # 4 bar plots
    bar_plot_king_crime(new_crime_df2)
    bar_plot_clark_crime(new_crime_df2)
    bar_plot_kitsap_crime(new_crime_df2)
    bar_plot_pierce_crime(new_crime_df2)


if __name__ == '__main__':
    main()
