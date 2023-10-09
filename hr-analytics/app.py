import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import altair as alt
import plotly.express as px


st.title ('HR Analytics')
st.sidebar.title ('HR Analytics')
page_mode = st.sidebar.selectbox ('Select Page', ['Data Cleaning', 'Data Visualization'])
# page_mode = 'Data Visualization'
# page_mode = 'Data Cleaning'

data = pd.read_csv ('HR-Employee-Attrition.csv')
column_names = data.columns.tolist ()
numerical_columns = data._get_numeric_data ().columns

@st.cache_resource
def get_unique_columns () :
    uniq_val_columns = []
    for item in column_names :
        if len (data [item].unique ()) == 1 :
            st.write (data [item].value_counts ())
            uniq_val_columns.append (item)
    return uniq_val_columns

@st.cache_resource
def my_value_counts (variable) :
    return data [variable].value_counts ()

@st.cache_resource
def plot_pie_chart (variable) :
    variable_counts = my_value_counts (variable)
    st.write (variable_counts)
    variable_values = variable_counts.index
    plt.pie (variable_counts, labels = variable_values, autopct = '%1.1f%%')
    plt.title (variable)
    st.pyplot ()

@st.cache_resource
def plot_donut_chart (variable) :
    variable_counts = my_value_counts (variable)
    st.write (variable_counts)
    variable_values = variable_counts.index
    plt.pie (variable_counts, labels = variable_values, wedgeprops = {'edgecolor' : 'white'})
    circle = patches.Circle ((0, 0), 0.70, fc = 'white')
    plt.gca ().add_patch (circle)
    plt.title (variable)
    plt.legend ()
    st.pyplot ()

@st.cache_resource
def plot_bar_chart (variable) :
    variable_counts = my_value_counts (variable)
    st.write (variable_counts)
    values = variable_counts.index
    heights = variable_counts.tolist ()
    colors = ['blue', 'green', 'orange', 'red', 'yellow', 'purple', 'brown', 'black']
    plt.bar (values, height = heights, width = 0.25, color = colors [:len (heights)])
    plt.xlabel (variable)
    plt.ylabel (str (variable) + ' Counts')
    plt.title (variable)
    st.pyplot ()

if page_mode == 'Data Cleaning' :

    st.subheader ('Data Cleaning')

    st.subheader ('HR Employee Attrition Dataset :')
    st.write (data.head ())

    st.subheader ('1. Redundant columns')
    st.subheader ('1.1. List of columns')
    st.write (data.columns)
    st.subheader ('1.2. List of numerical columns')
    num_data = data._get_numeric_data ()
    st.write (num_data.columns)
    st.subheader ('1.3. Correlation Matric')
    corr_matrix = num_data.corr ()
    st.write (corr_matrix)
    st.subheader ('1.4. Correlation of columns that have a high correlation coefficient (close to 1 or -1)')
    i = 1
    for col in num_data :
        for num_col in num_data :
            correlation = data[col].corr (data[num_col])
            # print (correlation)
            if ((correlation == - 1 or (correlation > -1 and correlation <= - 0.99)) or correlation == 1 or (correlation < 1 and correlation >= 0.99)) :
                if (col != num_col) :
                    st.markdown (f"The correlation between {col} and {num_col} is : {correlation}")
                    i = 0
    if (i == 1) :
        st.markdown ("There are no colums with a high correlation coefficient. So there not any redundant column to be deleted.")

    st.subheader ('2. Renaming columns')
    st.subheader ('3. Duplicates')
    st.write ('Number of duplicated data :', data.duplicated ().sum ())
    st.markdown ('There are no duplicates to be dropped')

    st.subheader ('4. Individual columns')
    st.markdown ('4.1. Identify individual columns')
    uniq_val_columns = get_unique_columns ()
    st.markdown ('4.2 Drop those columns')
    st.write ('Data shape before dropping individual columns :', data.shape)
    data = data.drop (uniq_val_columns, axis = 1)
    st.markdown ('The first 5 rows after dropping individual colomns')
    st.write (data.head ())
    data.head ()
    st.write ('Data shape after dropping individual columns :', data.shape)

    st.subheader ('5. NaN values')
    st.markdown ('Number of NaN values per column')
    st.write (data.isna ().sum ())
    st.write ('There is not a single NaN value.')

if page_mode == 'Data Visualization' :
    st.title ('Data Visualization')

    st.subheader ('1. Correlation map for all numeric variables')
    # Disable PyplotGlobalUseWarning warning
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Since there dropped columns, updata the variable numerical_columns
    uniq_val_columns = get_unique_columns ()
    data = data.drop (uniq_val_columns, axis = 1)
    numerical_columns = data._get_numeric_data ().columns
    correlation_matrix = data [numerical_columns].corr ()
    plt.figure (figsize = (20, 12))
    sns.heatmap (correlation_matrix, annot = True, cmap = 'Blues')
    plt.title ('Correlation Map')
    st.pyplot ()

    st.subheader ('2. Overtime')
    plot_pie_chart ('OverTime')

    st.subheader ('3. Marital Status')
    plot_bar_chart ('MaritalStatus')

    st.subheader ('4. Job Role')
    job_role = pd.DataFrame ({
        'Job Role' : my_value_counts ('JobRole').index,
        'Job Role Counts' : my_value_counts ('JobRole')
    })
    chart = alt.Chart (job_role).mark_line ().encode (
        x = 'Job Role',
        y = alt.Y('Job Role Counts', scale = alt.Scale (reverse = True))
    )
    st.altair_chart (chart, use_container_width = True)
    
    plot_pie_chart ('JobRole')
    
    st.subheader ('5. Gender')
    plot_donut_chart ('Gender')

    st.subheader ('6. Education Field')
    plot_bar_chart ('EducationField')

    st.subheader ('7. Department')
    plot_pie_chart ('Department')

    st.subheader ('8. Business Travel')
    plot_donut_chart ('BusinessTravel')

    st.subheader ('9. Relation between `Over Time` and `Age`')
    colors = ['blue', 'orange']
    x = data ['OverTime']
    sns.boxplot (x = x, y = data ['Age'], hue = x, palette = colors, legend = False)
    plt.xlabel ('Over Time')
    plt.ylabel ('Age')
    plt.title ('Relation between OverTime and Age')
    st.pyplot ()

    st.subheader ('10. Total Working Years')
    fig, ax = plt.subplots ()
    ax.hist (data ['TotalWorkingYears'], bins = 15)
    st.pyplot ()
    st.caption ('TotalWorkingYears')

    st.subheader ('11. Education Level')
    plot_bar_chart ('Education')

    st.subheader ('12. Number Of Companies Worked')
    number_companies = my_value_counts ('NumCompaniesWorked')
    companies = number_companies.index
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'cyan']
    st.write (number_companies)
    plt.scatter (number_companies, companies, s = number_companies, c = colors, alpha = 0.5)
    st.pyplot ()

    st.subheader ('13. Distance From Home')
    plot_bar_chart ('DistanceFromHome')

st.markdown ('Made by H. Moustapha Ousmane')
