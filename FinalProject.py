'''
Created on Apr 24, 2024

@author: agood

Name: Alexis Goodney
CS230: Section 2
Data: Nuclear Explosions

Description: Description:
This program provides an interface for exploring and analyzing nuclear explosions data. 
It allows users to filter explosions based on magnitude, time frame, and weapon types, 
and visualize the filtered data through time plots and magnitude distribution histograms. 
Additionally, users can view summary statistics of nuclear tests, search for specific 
test names, and explore deployment locations of US-made nuclear weapons through an 
interactive map.

'''

import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

# load the nuclear explosions data from a CSV file. 
df = pd.read_csv(r"C:\Users\agood\OneDrive - Bentley University\eclipse-workspace\week-13\nuclear_explosions.csv")

# set configuration for the Streamlit page.
st.set_page_config(layout = 'wide', page_title = 'Nuclear Explosions Project', page_icon = ':bomb:')


def magnitude_query(min_magnitude, max_magnitude=10):
    """
    Prompt user to input minimum and maximum magnitude for filtering.

    Args:
        min_magnitude (int): Minimum magnitude value.
        max_magnitude (int, optional): Maximum magnitude value. Defaults to 10.

    Returns:
        tuple: Minimum and maximum magnitude values.
    """
    # display subheader for the magnitude query section
    st.subheader('Magnitude Inquery: enter min and max value')
    
    # define allowable min and max value rage using sliders
    min_value, max_value = st.slider('Magnitude Range', min_value=0, max_value=10, value=(min_magnitude, max_magnitude))
    
    # return selected min/max magnitude values
    
    # return selected min/max magnitude values
    return min_value, max_value


def time_frame_query(start_date, end_date):
    """
    Prompt the user to input the beginning and end dates for filtering events within a specified time frame.

    Args:
        start_date (datetime.date): The initial start date for the time frame.
        end_date (datetime.date): The initial end date for the time frame.

    Returns:
        tuple: A tuple containing the start and end dates selected by the user.
    """
    
    # display a subheader for the time query section
    st.subheader('Timeline Inquery: enter beginning and end date')
    
    # define allowable min/max dates for selection
    min_date = datetime.date(1945, 7, 16)
    max_date = datetime.date(1969, 12, 29)
    
    # prompt user to input start/end date within specified range 
    start_date = st.date_input('Start Date', start_date, min_value = min_date, max_value = max_date)
    end_date = st.date_input('End Date', end_date, min_value = start_date, max_value = max_date)
    
    # return selected start and end dates
    return start_date, end_date


def type_based_query(weapon_types): 
    """
    Prompt the user to select weapon types for filtering.

    Args:
        weapon_types (list): List of available weapon types.

    Returns:
        list: List of selected weapon types.
    """
    # display subheader for deployment method query
    st.subheader('Deployment Method: choose weapon types')
    weapon_types = ['Airdrop', 'Tower', 'Uw', 'Surface', 'Ship', 'Atmosph', 'Barge', 'Balloon', 'Shaft', 'Rocket', 'Tunnel', 'Space', 'Crater', 'Gallery', 'Ug', 'Shaft/Gr', 'Shaft/Gr', 'Mine']
    
    # present the user with multiselect option to choose
    selected_types = st.multiselect('Select Weapon Types', weapon_types)
    
    # filter out empty or None values 
    selected_types = [weapon for weapon in selected_types if weapon]
    
    # if weapon types selected, they're displayed 
    if selected_types:
        st.write('Selected Weapon Types:')
        for weapon in selected_types: 
            st.write(weapon)
            
    # return the list of selected weapon types
    return selected_types


def filter_data(df, min_magnitude, max_magnitude, start_date, end_date, selected_types, sort_order = 'ascending'):
    """
    Filter the given DataFrame based on specified criteria.

    Args:
        df (pandas.DataFrame): DataFrame containing the data to be filtered.
        min_magnitude (float): Minimum magnitude value for filtering.
        max_magnitude (float): Maximum magnitude value for filtering.
        start_date (datetime.date): Start date for filtering events within a time frame.
        end_date (datetime.date): End date for filtering events within a time frame.
        selected_types (list): List of selected weapon types for filtering.
        sort_order (str, optional): Sorting order for the filtered DataFrame. Defaults to 'ascending'.

    Returns:
        pandas.DataFrame: Filtered DataFrame containing refined nuclear explosions data.
    """
    # display subheader for refined nuclear explosions
    st.subheader('Refined Nuclear Explosions: ')
    
    # filter dataframe based on min/max magnitude values
    df_filtered = df[(df['Data.Magnitude.Body'] >= min_magnitude) & (df['Data.Magnitude.Body'] <= max_magnitude)]
    
    # convert date columns to proper datetime format & filter events within users range
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date.Year'].astype(str) + '-' + df_filtered['Date.Month'].astype(str) + '-' + df_filtered['Date.Day'].astype(str))
    df_filtered.drop(columns=['Date.Day', 'Date.Month', 'Date.Year'], inplace=True)  # Remove separate date columns
    df_filtered = df_filtered[(df_filtered['Date'] >= pd.to_datetime(start_date)) & (df_filtered['Date'] <= pd.to_datetime(end_date))]
    
    # filter the dataframe based on selected weapon types
    if selected_types:
        df_filtered = df_filtered[df_filtered['Data.Type'].isin(selected_types)]
    
    # sort the dataframe based on specified sort order 
    if sort_order == 'ascending':
        df_filtered.sort_values(by='WEAPON DEPLOYMENT LOCATION', ascending=True, inplace=True)
    else:
        df_filtered.sort_values(by='WEAPON DEPLOYMENT LOCATION', ascending=False, inplace=True)
 
    # select desired columns for filtered dataframe 
    desired_columns = ['WEAPON SOURCE COUNTRY', 'WEAPON DEPLOYMENT LOCATION', 'Location.Cordinates.Latitude', 'Location.Cordinates.Longitude' ,   'Data.Magnitude.Body','Data.Type', 'Date']
    df_filtered = df_filtered[desired_columns]
    
    # return filtered dataframe
    return df_filtered


def time_plot(df, color = 'purple'):
    """
    Create a time plot showing the number of nuclear explosions over time.

    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        color (str, optional): Color of the plot. Defaults to 'purple'.
    """
    # convert date columns to proper date format 
    df['Date'] = pd.to_datetime(df['Date.Year'].astype(str) + '-' + df['Date.Month'].astype(str) + '-' + df['Date.Day'].astype(str))
    # sample data by year and calculate the number of explosions per year 
    explosions_per_year = df.resample('Y', on='Date').size()
    
    # create fig and axis object
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # plot the data on the axis 
    explosions_per_year.plot(ax=ax, color=color)
    
    # set labels and title for the plot
    plt.xlabel('Year')
    plt.ylabel('Number of Explosions')
    plt.title('Number of Nuclear Explosions Over Time')
    
    # display the plot using Streamlit's py.plot() function
    st.pyplot(fig)


def magnitude_plot(data, color = 'purple'):
    """
    Create a histogram plot showing the frequency distribution of magnitudes.

    Args:
        data (pandas.Series or array-like): Magnitude data to plot.
        color (str, optional): Color of the plot. Defaults to 'purple'.
    """
    # create new figure and axis object 
    fig, ax = plt.subplots(figsize = (8,4))
    
    # create histogram of the magnitude data 
    hist, bins, _ = plt.hist(data, bins=10, color=color)
    
    # plot the histogram bars with specified color 
    ax.bar(bins[:-1], hist, width=(bins[1]-bins[0]), align='edge', color = color)
    
    # set labels and title for the plot 
    ax.set_xlabel('Magnitude')
    ax.set_ylabel('Frequency')
    ax.set_title('Frequency Distribution of Magnitude')
    
    #display the plot using Streamlit's st.pyplot()function
    st.pyplot(fig)


def create_interactive_map(df):
    """
    Create an interactive map displaying US-made nuclear weapons deployment locations.

    Args:
        df (pandas.DataFrame): DataFrame containing the nuclear weapons data.
    """
    # set title and description for the map
    st.title('Interactive Map of US Made Nuclear Weapons')
    st.write('This map focuses in on Nevada, many US made weapons are used at the Nevada Test Site.')
    st.write('The NTS is a nuclear testing site operated by the U.S. Department of Energy.')
    st.write('Feel free to move around the map there are US weapons used in Japan, Russia, and more!')
    
    # filter the dataframe to include on US-made weapons
    df_us = df[df['WEAPON SOURCE COUNTRY'] == 'USA']
    df_us = df_us.rename(columns={'Location.Cordinates.Latitude': 'lat', 'Location.Cordinates.Longitude' : 'lon'})

    # set initial view state for the map
    view_state = pdk.ViewState(
        latitude=37.04, 
        longitude=-116.16,
        zoom = 8,
        pitch=50
    )

    # define the scatterplot layer 
    scatterplot_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_us,
        get_position=['lon', 'lat'],
        get_radius=1000,
        get_fill_color=[0, 0, 255],
        pickable=True)
    
    # define the tooltip for displaying information on hover   
    tool_tip={'html': '<b>WEAPON DEPLOYMENT LOCATION:</b> {WEAPON DEPLOYMENT LOCATION}<br>'
                    '<b>Latitude:</b> {lat}<br>'
                    '<b>Longitude:</b> {lon}<br>'
                    '<b>Magnitude:</b> {Data.Magnitude.Body}<br>'
                    '<b>Type:</b> {Data.Type}'
        }

    # create the map using PyDeck
    map_deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[scatterplot_layer], 
        tooltip = tool_tip
    )
    # display the map using Streamlit's st.pydeck_chart() function
    st.pydeck_chart(map_deck)
    
    
def summary_statistics(df):
    """
    Display summary statistics of nuclear explosions.

    Args:
        df (pandas.DataFrame): DataFrame containing the nuclear explosions data.
        min_magnitude (float): Minimum magnitude threshold for filtering explosions.
    """

    # display subheader for summary statistics section
    st.subheader('Summary Statistics')
    
    # display the total number of explosions, min magnitude, and max magnitude
    st.write('Total Number of Explosions:', len(df))
    st.write('Maximum Magnitude:', df['Data.Magnitude.Body'].max())
    st.write('Minimum Magnitude:', df['Data.Magnitude.Body'].min())


def text_search(search_term):
    """
    Perform a text search on the DataFrame and display search results.

    Args:
        search_term (str): Search term to look for in the 'Data.Name' column.
    """
    
    # perform a text search on the dataframe using specified search term inputed
    search_results = df[df['Data.Name'].str.contains(search_term, case = False)]
    
    # check if any search results were found
    if not search_results.empty:
        # display subheader for search results section
        st.subheader('Search Results:')
        
        # define desired columns to display in results
        desired_columns = ['WEAPON SOURCE COUNTRY', 'WEAPON DEPLOYMENT LOCATION','Data.Magnitude.Body','Data.Name','Data.Purpose', 'Data.Type']
        # filter search results dataframe to include only desired columns
        search_results = search_results[desired_columns]
        
        # display search results
        st.write(search_results)
    else:
        # display message indicating no results were found
        st.write('No matching results found.')
        
        
def main():
    
    # sidebar navigation options
    page_options = ['Home Page', 'Explosion Finder', 'Data Visualizations', 'Nuclear Test Statistics', 'Interactive Map']
    selected_page = st.sidebar.selectbox(options = page_options, label = 'Select Page')
    min_magnitude = 0
    sort_order = 'ascending'
    
    if selected_page == 'Home Page':
        # display home page content 
        st.title('Nuclear Explosions Project')
        st.write('By Alexis Goodney')
        st.write('Welcome to my program!')
        st.write('Please visit the sidebar for navigation.')
        st.image('https://t4.ftcdn.net/jpg/05/55/89/11/360_F_555891196_5tuFqpGHnlTgv1AhiE4nezTckQtdc8wl.jpg')
        
    elif selected_page == 'Explosion Finder':
        # perform explosion filtering
        st.title('Nuclear Explosion Finder')
        min_magnitude, max_magnitude = magnitude_query(0, 10)
        
        start_date, end_date = time_frame_query(datetime.date(1945, 7, 16), datetime.date(1969, 12, 29))
        selected_types = type_based_query(df['Data.Type'])
        
        sort_order = st.radio("Sort Order based on Deployment Location", options=['Ascending', 'Descending'], index=0 if sort_order == 'ascending' else 1)
        sort_order = 'ascending' if sort_order == 'Ascending' else 'descending'

        filtered_df = filter_data(df, min_magnitude, max_magnitude, start_date, end_date, selected_types, sort_order)
        st.dataframe(filtered_df)

    elif selected_page == 'Data Visualizations':
        # display data charts and graphs 
        st.title('Data Visualizations')
        time_plot(df, color = 'purple')
        magnitude_plot(df['Data.Magnitude.Body'], color = 'purple')

    
    elif selected_page =='Nuclear Test Statistics':
        # display nuclear test statistics 
        st.title('Nuclear Test Statistics')
        summary_statistics(df)
        
        st.header('Enter Name of Nuclear Test for Specific Stats')
        search_term = st.text_input('Enter search term:')
        if st.button('Search'):
            text_search(search_term)
            
        
    elif selected_page == 'Interactive Map':
        # display interactive map 
        df_us = df[df['WEAPON SOURCE COUNTRY'] == 'USA']
        create_interactive_map(df_us)


main()