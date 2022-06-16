"""
Caroline Ding
CSE 163
This is a test file to test all the methonds created in pop_density.py
"""


import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pop_density
from cse163_utils import assert_equals


def test_select_pop_df(lst_column_names_pop, pop_df):
    """
    Test the select pop df method.
    """
    get_select_pop_df = \
        pop_density.select_pop_df(lst_column_names_pop, pop_df)
    assert_equals(120, get_select_pop_df.loc[0, 'POPDEN_2019'])


def test_change_pop_df_shape(lst_column_names_pop, get_select_pop_df):
    """
    Test the change pop df shape method.
    """
    update_select_pop_df = \
        pop_density.change_pop_df_shape(lst_column_names_pop,
                                        get_select_pop_df)
    assert_equals('ASOTIN', update_select_pop_df.loc[2, 'COUNTY_NAME'])


def test_select_crime_df(crime_df):
    """
    Test select crime dataframe method.
    """
    get_select_crime_df = pop_density.select_crime_df(crime_df)
    assert_equals(68.4, get_select_crime_df.loc[3, 'RATE'])
    assert_equals('2020', get_select_crime_df.loc[1, 'INDEXYEAR'])


def test_merge_pop_crime_df(update_select_pop_df, get_select_crime_df):
    """
    Test merge pop crime df method.
    """
    merge_df = pop_density.merge_pop_crime_df(update_select_pop_df,
                                              get_select_crime_df)
    assert_equals('ADAMS', merge_df.loc[1, 'COUNTY'])
    assert_equals(300, merge_df.loc[3, 'POPDEN'])


def test_county_pop_greater_100(merge_df):
    """
    Test county pop greater 100 method.
    """
    assert_equals(['ASOTIN'],
                  pop_density.county_pop_greater_100(merge_df))


def test_scattar_plot_df(merge_df, lst_county_name):
    """
    Test scatter plot df method.
    """
    get_scatter_plot_df = \
        pop_density.scattar_plot_df(merge_df, lst_county_name)
    assert_equals('ASOTIN', get_scatter_plot_df.loc[0, 'COUNTY_NAME'])
    assert_equals(68.4, get_scatter_plot_df.loc[1, 'RATE'])


def test_top4_pop_county_crime_df(lst_county_names_bar, crime_df2):
    """
    Test top4 pop county crime df method.
    """
    get_update_crime_df2 = \
        pop_density.top4_pop_county_crime_df(lst_county_names_bar,
                                             crime_df2)
    assert_equals(100, get_update_crime_df2.loc[0, 'MURDER'])
    assert_equals(300, get_update_crime_df2.loc[2, 'MURDER'])
    assert_equals(400, get_update_crime_df2.loc[1, 'THEFT'])


def test_new_shape_crime_df(update_crime_df2):
    """
    Test new shape crime df method.
    """
    get_update_crime_df2 = \
        pop_density.new_shape_crime_df(update_crime_df2)
    assert_equals('PIERCE', get_update_crime_df2.loc[19, 'COUNTY'])
    assert_equals(40, get_update_crime_df2.loc[6, 'value'])


def main():
    # create two small dataframe
    lst_dic_small_pop = {'COUNTY_NAME': ['Adams', 'Asotin'],
                         'POPDEN_2019': [120, 200],
                         'POPDEN_2020': [90, 300]}
    small_pop_df = pd.DataFrame(lst_dic_small_pop)

    lst_dic_small_crime = {'COUNTY': ['ADAMS', 'ADAMS', 'ADAMS',
                                      'ASOTIN', 'ASOTIN'],
                           'INDEXYEAR': [2018, 2019, 2020, 2019, 2020],
                           'LOCATION': ['Office', 'COUNTY TOTAL',
                                        'COUNTY TOTAL', 'COUNTY TOTAL',
                                        'COUNTY TOTAL'],
                           'RATE': [62.88, 100.5, 102.7, 66.2, 68.4]}
    small_crime_df = pd.DataFrame(lst_dic_small_crime)

    # list of columns that we are going to use in scatter plot and line plots
    lst_column_names_pop = ['COUNTY_NAME', 'POPDEN_2019', 'POPDEN_2020']

    test_select_pop_df(lst_column_names_pop, small_pop_df)
    get_select_pop_df = \
        pop_density.select_pop_df(lst_column_names_pop, small_pop_df)

    test_change_pop_df_shape(lst_column_names_pop, get_select_pop_df)
    update_select_pop_df = \
        pop_density.change_pop_df_shape(lst_column_names_pop,
                                        get_select_pop_df)

    test_select_crime_df(small_crime_df)
    get_select_crime_df = pop_density.select_crime_df(small_crime_df)

    test_merge_pop_crime_df(update_select_pop_df, get_select_crime_df)
    merge_df = pop_density.merge_pop_crime_df(update_select_pop_df,
                                              get_select_crime_df)

    test_county_pop_greater_100(merge_df)
    lst_county_name = ['ASOTIN']

    test_scattar_plot_df(merge_df, lst_county_name)
    get_scatter_plot_df = \
        pop_density.scattar_plot_df(merge_df, lst_county_name)

    # plot the small interactive scatter graph
    small_fig1 = px.scatter(get_scatter_plot_df, x="POPDEN", y="RATE",
                            color="COUNTY_NAME", trendline="ols",
                            trendline_scope="overall",
                            trendline_color_override="black",
                            labels={"POPDEN": "Population Density",
                                    "RATE": "Crime Rate per 1,000 Residents",
                                    "COUNTY_NAME": "County names"},
                            title="Relationship Between Population Density "
                                  "and Crime Rate in 5 Counties with the "
                                  "Highest Population Density")
    small_fig1.show()

    lst_county_names_bar = ['KING', 'CLARK', 'KITSAP', 'PIERCE']

    # create another small crime dataframe that we are going to use in
    # bar plots.
    lst_dic_small_crime2 = {'COUNTY': ['KING', 'CLARK', 'KITSAP', 'PIERCE'],
                            'INDEXYEAR': [2020, 2020, 2020, 2020],
                            'LOCATION': ['COUNTY TOTAL', 'COUNTY TOTAL',
                                         'COUNTY TOTAL', 'COUNTY TOTAL'],
                            'RATE': [62.88, 100.5, 102.7, 66.2],
                            'POPULATION': [0, 0, 0, 0],
                            'TOTAL': [100, 100, 100, 100],
                            'PRSNTOTAL': [0, 0, 0, 0],
                            'PRSNRATE': [0, 0, 0, 0],
                            'PRPRTYTOTAL': [0, 0, 0, 0],
                            'PRPRTYRATE': [0, 0, 0, 0],
                            'MURDER': [100, 200, 300, 400],
                            'ASSAULT': [20, 30, 40, 50],
                            'ARSON': [10, 8, 9, 5],
                            'ROBBERY': [30, 40, 50, 60],
                            'THEFT': [300, 400, 600, 700]}
    small_crime_df2 = pd.DataFrame(lst_dic_small_crime2)

    test_top4_pop_county_crime_df(lst_county_names_bar, small_crime_df2)
    update_crime_df2 = \
        pop_density.top4_pop_county_crime_df(lst_county_names_bar,
                                             small_crime_df2)

    test_new_shape_crime_df(update_crime_df2)
    new_update_crime_df2 = \
        pop_density.new_shape_crime_df(update_crime_df2)

    # create a bar plot with the small crime dataframe
    small_king_crime_df = \
        new_update_crime_df2.loc[new_update_crime_df2.COUNTY == 'KING']
    small_king_crime_df2 = \
        small_king_crime_df.nlargest(n=5, columns=['value'], keep='all')
    sns.catplot(x="value", y="variable", data=small_king_crime_df2, kind="bar",
                palette="Purples_r")
    plt.xlabel('Crime Count')
    plt.ylabel('Crime Types')
    plt.savefig('plots/pop/test_bar_plot_king_crime.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
