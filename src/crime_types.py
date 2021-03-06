"""
Iris Zhou
CSE 163
This file contains methods for loading and cleaning crime data on Washington
state counties and geodata on county boundaries. It also contains methods
for adding and mutating the necessary columns for data analysis, and methods
for visualizing most frequently reported types of crime and trends over
time for counties.

Running the main method will open interactive visualiations made using the
library plotly in a web browswer.
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import seaborn as sns
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

sns.set()


SHOW_PLOTS = False


def load_and_clean_crime_data(file_path):
    """
    Loads crime data from the given file path, cleans column names for easier
    analysis, filters to only include county totals, and returns as a Pandas
    data frame.
    """
    crime_df = pd.read_csv(file_path)
    crime_df.columns = crime_df.columns.str.lower()
    crime_df.rename(columns={'indexyear': 'year'}, inplace=True)
    crime_df = crime_df[crime_df['location'] == 'COUNTY TOTAL']
    crime_df = crime_df.iloc[:, np.r_[:2, 3, 5, 8:16, 18:26, 28:33]]
    return crime_df


def load_and_clean_county_shapes(file_path):
    """
    Loads shape data of Washington counties from the given file path,
    cleans column names for better usability, filters for relevant columns,
    and returns as a GeoDataFrame.
    """
    counties = gpd.read_file(file_path)
    counties = counties.rename({'JURISDIC_1': 'name'}, axis=1)
    counties = counties[['name', 'geometry']]
    counties['name'] = counties['name'].str.upper()
    counties = counties.to_crs(4326)  # reproject to geographic CRS
    return counties


def get_crime_totals(crime_df):
    """
    Given crime dataframe, appends column of total reported offenses.
    """
    crime_df['crime_totals'] = crime_df.iloc[:, 4:].sum(axis=1).astype('int')


def get_crime_type_rates(crime_df):
    """
    Given dataframe of crime data, recomputes counts of reported offenses for
    each offense category as proportions out of total reported offenses.
    Returns as new dataset.
    """
    crime_rate_df = crime_df
    crime_rate_df.iloc[:, 4:-1] = \
        crime_rate_df.iloc[:, 4:-1].div(crime_rate_df.crime_totals, axis=0)
    return crime_rate_df


def pivot_rate_data(rate_2020_df):
    """
    Given dataframe of crime rates, reshapes dataframe into longer format that
    can be used for plotting, and returns resulting dataframe.
    """
    pivot_2020_df = rate_2020_df.iloc[:, np.r_[0, 4:25]]
    pivot_2020_df = pd.melt(pivot_2020_df, id_vars=['county'],
                            var_name='crime_type', value_name='prop')
    return pivot_2020_df


def get_top_crime_type(pivot_2020_df):
    """
    Given pivoted dataframe of crime rates, returns new data frame of the most
    frequently reported type of crime and the proportion of that type to
    the total offenses reported for each county.
    """
    index = pivot_2020_df.groupby('county')['prop'].idxmax()
    top_type_df = pivot_2020_df.loc[index, ['county', 'crime_type', 'prop']]
    return top_type_df


def get_second_top_crime_type(pivot_2020_df, top_type_df):
    """
    Given pivoted dataframe of crime rates and dataframe of most reported
    types of crime, returns new data frame of the second most frequently
    reported type of crime and the proportion of that type to
    the total offenses reported for each county.
    """
    # Filter out top crime types in each county
    not_top_type_df = \
        pivot_2020_df[~pivot_2020_df['prop'].isin(top_type_df['prop'])]
    index = not_top_type_df.groupby('county')['prop'].idxmax()
    top2_type_df = not_top_type_df.loc[index,
                                       ['county', 'crime_type', 'prop']]
    return top2_type_df


def plot_top_crime_types(crime_type_df, counties, plot_title):
    """
    Given dataframe of top crime types for each Washington state county
    and GeoDataFrame of geometries of counties, plots interactive map colored
    by top crime type in each county. Titles the map according
    to the given plot_title.

    If SHOW_PLOTS is true, opens resulting interactive map in a web browser.
    Returns map.
    """
    map_df = counties.merge(crime_type_df, left_on='name', right_on='county')
    map_df = map_df.set_index('name')

    map = px.choropleth_mapbox(map_df,
                               geojson=map_df.geometry,
                               locations=map_df.index,
                               color="crime_type",
                               center={"lat": 47.3254, "lon": -120.7401},
                               mapbox_style="carto-positron",
                               zoom=5.4, width=750, height=450,
                               title=plot_title,
                               hover_name='county',
                               hover_data=['crime_type', 'prop'])
    map.update_layout(margin={"r": 30, "t": 50, "l": 30, "b": 20},
                      legend_title_text='Crime Type')
    if SHOW_PLOTS:
        map.show()
    return map


def plot_crime_type_rate(crime_type, pivot_2020_df, counties):
    """
    Given a crime type as a string, a pivoted dataframe of crime rates, and
    a GeoDataFrame of Washington state counties, plots the relative
    proportion of total crimes that were of that crime type in each county on
    an interactive map.

    If SHOW_PLOTS is true, opens resulting interactive map in a web browser.
    Returns map.
    """
    is_type = pivot_2020_df['crime_type'] == crime_type
    crime_rate_map_df = counties.merge(pivot_2020_df[is_type],
                                       left_on='name', right_on='county')
    crime_rate_map_df = crime_rate_map_df.set_index('name')

    color_scale = px.colors.sequential.Viridis
    crime_type = crime_type.replace('_', ' ')
    crime_type = crime_type[0].upper() + crime_type[1:]
    plot_title = crime_type  # + ' rate in WA counties in 2020'
    map = px.choropleth_mapbox(crime_rate_map_df,
                               geojson=crime_rate_map_df.geometry,
                               locations=crime_rate_map_df.index,
                               color="prop",
                               color_continuous_scale=color_scale,
                               center={"lat": 47.3254, "lon": -120.7401},
                               mapbox_style="carto-positron",
                               zoom=4.5, width=380, height=250,
                               title=plot_title,
                               hover_name='county',
                               hover_data=['prop'])
    map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    if SHOW_PLOTS:
        map.show()
    return map


def pop_vs_crime_rate(crime_type, rate_2020_df, with_king_county=True):
    """
    Given a crime type as a string and a DataFrame of the relative rates of
    crime types and population counts for counties, plots a regression line of
    relationship between population and crime rate for type.
    If with_king_county is True or unspecified, plot will include King county.
    If with_king_county is False, plot will exclude King county.

    If SHOW_PLOTS is true, opens resulting interactive plot in a web browser.
    Returns plot.
    """
    plot_df = rate_2020_df
    plot_title = 'Relationship between population and<br>'
    plot_title += crime_type.lower() + ' rate in 2020 '

    if with_king_county:
        plot_title += '(with King County)'
    else:
        plot_df = rate_2020_df[rate_2020_df['county'] != 'KING']
        plot_title += '(without King County)'

    plot = px.scatter(plot_df, x='population', y=crime_type, trendline='ols',
                      hover_name='county',
                      height=400,
                      width=400,
                      title=plot_title)
    plot.update_layout(margin={"r": 80, "t": 80, "l": 0, "b": 0})
    if SHOW_PLOTS:
        plot.show()
    return plot


def plot_prop_over_time(county, crime_rate_df, top_5=True):
    """
    Given the name of a Washington county and a DataFrame of crime data
    and the relative rates of crime types, plots interactive chart of
    change in relative rates of criminal offenses in the given county
    over time.
    If top_5 is True or unspecifed, only plots the top 5 most frequently
    reported crime types.
    If top_5 is False, plots all crime types but the top 5.

    If SHOW_PLOTS is true, opens interactive plot in a web browser.
    Returns plot.
    """
    county = county.upper()
    county_crime_df = crime_rate_df[crime_rate_df['county'] == county]
    melt_df = county_crime_df.iloc[:, np.r_[1:2, 4:25]]
    melt_df = pd.melt(melt_df, id_vars=['year'],
                      var_name='crime_type', value_name='prop')
    county_2020_df = melt_df[melt_df['year'] == 2020]
    county_2020_df = county_2020_df.sort_values(by='prop',
                                                ascending=False).head(5)
    top_5_crime_types = county_2020_df['crime_type']

    plot_title = 'Change in proportion of '
    if top_5:
        plot_df = melt_df[melt_df['crime_type'].isin(top_5_crime_types)]
        plot_title += 'top 5 '
        plot_height = 350
        plot_width = 400
    else:
        plot_df = melt_df[~melt_df['crime_type'].isin(top_5_crime_types)]
        plot_title += 'non-top 5 '
        plot_height = 450
        plot_width = 450
    plot_title += 'crime types <br>in ' + county[0] + county[1:].lower() + \
        ' county over time'

    plot = px.line(plot_df, x='year', y='prop', color='crime_type',
                   markers=True, width=plot_width, height=plot_height,
                   title=plot_title)
    plot.update_layout(margin={"r": 80, "t": 80, "l": 0, "b": 0},
                       legend_title_text='Crime Type')
    if SHOW_PLOTS:
        plot.show()
    return plot


def main():
    crime_data_path = 'data/NIBRS_crime.csv'
    wa_shape_path = 'data/wa_shapefiles/WA_County_Bndys.shp'

    # Load and clean datasets
    crime_df = load_and_clean_crime_data(crime_data_path)
    counties = load_and_clean_county_shapes(wa_shape_path)

    # Add and mutate necessary columns, and create new dataframes
    get_crime_totals(crime_df)
    crime_rate_df = get_crime_type_rates(crime_df)
    rate_2020_df = crime_rate_df[crime_rate_df['year'] == 2020]
    pivot_2020_df = pivot_rate_data(rate_2020_df)

    # 1. What types of crime occur most frequently in different counties?

    # Find first and second most frequent types of offenses reported
    top_type_df = get_top_crime_type(pivot_2020_df)
    top2_type_df = get_second_top_crime_type(pivot_2020_df, top_type_df)

    # WARNING: maps will open in web browser
    top_title = 'Most frequent type of crime in each county in 2020'
    top_map = plot_top_crime_types(top_type_df, counties, top_title)
    top2_title = 'Second most frequent type of crime in each county in 2020'
    top2_map = plot_top_crime_types(top2_type_df, counties, top2_title)

    # 2. How does the proportion of criminal offenses of different types vary
    #    across counties?

    # Plot relative rate of crime types for Washington counties in 2020
    # WARNING: maps will open in web browser
    theft_map = plot_crime_type_rate('theft', pivot_2020_df, counties)
    assault_map = plot_crime_type_rate('assault', pivot_2020_df, counties)
    dop_map = plot_crime_type_rate('destruction_of_property',
                                   pivot_2020_df, counties)
    burglary_map = plot_crime_type_rate('burglary', pivot_2020_df, counties)

    # 2. (subquestion) Is there a relationship between population and the
    #                  proportion of a crime type?

    # Plot regression line between population and proportion of crime type
    # WARNING: maps will open in web browser
    assault_reg_king = pop_vs_crime_rate('assault', rate_2020_df)
    assault_reg_noking = pop_vs_crime_rate('assault', rate_2020_df, False)
    theft_reg_king = pop_vs_crime_rate('theft', rate_2020_df)
    theft_reg_noking = pop_vs_crime_rate('theft', rate_2020_df, False)

    # 3. How has relative frequency of different types of crime changed over
    #    time different counties?

    # WARNING: maps will open in web browser
    # Plot top 5 and non-top 5 crime types over time in King county
    king_top5 = plot_prop_over_time('King', crime_rate_df)
    king_not_top5 = plot_prop_over_time('King', crime_rate_df, False)

    # Plot top 5 crime types over time in other counties
    pierce_top5 = plot_prop_over_time('Pierce', crime_rate_df)
    stevens_top5 = plot_prop_over_time('Stevens', crime_rate_df)
    jefferson_top5 = plot_prop_over_time('Jefferson', crime_rate_df)
    garfield_top5 = plot_prop_over_time('Garfield', crime_rate_df)
    columbia_top5 = plot_prop_over_time('Columbia', crime_rate_df)

    # Save plots to plotly account
    chart_studio.tools.set_credentials_file(username='irisz1',
                                            api_key='KpywulqM2TABw3Yt5hRo')
    py.plot(assault_reg_king, filename='assault_reg_king', auto_open=False)
    py.plot(assault_reg_noking, filename='assault_reg_noking', auto_open=False)
    py.plot(theft_reg_king, filename='theft_reg_king', auto_open=False)
    py.plot(theft_reg_noking, filename='theft_reg_noking', auto_open=False)
    py.plot(king_top5, filename='king_top5', auto_open=False)
    py.plot(king_not_top5, filename='king_not_top5', auto_open=False)

    py.plot(pierce_top5, filename='pierce_top5', auto_open=False)
    py.plot(stevens_top5, filename='stevens_top5', auto_open=False)
    py.plot(jefferson_top5, filename='jefferson_top5', auto_open=False)
    py.plot(garfield_top5, filename='garfield_top5', auto_open=False)
    py.plot(columbia_top5, filename='columbia_top5', auto_open=False)

    # Generate iframe code to embed plots from plotly account
    iframe_code = []
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/4/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/8/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/10/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/12/'))
    iframe_code.append('')
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/14/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/18/'))
    iframe_code.append('')
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/20/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/22/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/24/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/26/'))
    iframe_code.append(tls.get_embed('https://plotly.com/~irisz1/28/'))

    with open('plots/plotly/iframe_code.txt', 'w') as f:
        for embed in iframe_code:
            f.write(embed)
            f.write('\n')

    # Generate iframe code for maps saved locally
    top_map.write_html('plots/plotly/top_map.html', full_html=False)
    top2_map.write_html('plots/plotly/top2_map.html', full_html=False)

    theft_map.write_html('plots/plotly/theft_map.html', full_html=False)
    assault_map.write_html('plots/plotly/assault_map.html', full_html=False)
    dop_map.write_html('plots/plotly/dop_map.html', full_html=False)
    burglary_map.write_html('plots/plotly/burglary_map.html', full_html=False)


if __name__ == '__main__':
    main()
