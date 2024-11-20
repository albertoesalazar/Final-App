import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from data_preprocessing import preprocess_data # Import the created Data_Preprocesing.py file 

df = pd.read_csv("Affordable_Housing_by_Town_2011-2023_2024.csv")

df = preprocess_data(df) # data pre-procesing file will update DataFrame automatically


# Interactive Widgets

with st.sidebar:
    county_filter = st.sidebar.multiselect("Select County(s):", options=df['County'].unique(), default=df['County'].unique()) # Can select single/multiple counties for analysis
    year_filter = st.sidebar.slider("Select Year Range:", int(df['Year'].min()), int(df['Year'].max()), (2020, 2022)) # Implemented slider for users to select specific year ranges
    filtered_df = df[(df['County'].isin(county_filter)) & (df['Year'].between(year_filter[0], year_filter[1]))]
    columns_for_radio = df.columns[2:7] # Ct programs listed as radio buttons 
    selected_column = st.radio("Select a column for analysis:", options=columns_for_radio) 

# Line chart

st.title("CT Affordable Housing Impact")

st.subheader(f"{selected_column} Over Time") # The line chart will update automatically when a housing program is selected from the radio buttons 
fig = px.line(
    filtered_df,
    x='Year',
    y=selected_column,
    color='Town',
    markers=True,
    title=f"{selected_column} Over Time",
    labels={"Year": "Year", selected_column: selected_column},
    hover_data=['Town', 'Year', selected_column]
)
fig.update_layout(
    width=800,
    height=400,
    legend_title="Town",
    title_x=0.5
)
st.plotly_chart(fig)

# A table is also implemented to display the percent of affordable housing for clarity

# Can filter based on the year range chosen from the slider

st.subheader("Towns with Highest and Lowest Affordable Housing Percentages")
highest = filtered_df.loc[filtered_df.groupby('Year')['Percent Affordable'].idxmax()]
lowest = filtered_df.loc[filtered_df.groupby('Year')['Percent Affordable'].idxmin()]

st.write("### Highest Percent Affordable")
st.table(highest[['Year', 'Town', 'Percent Affordable']])
st.write("### Lowest Percent Affordable")
st.table(lowest[['Year', 'Town', 'Percent Affordable']])

# Will plot Folium map of Highest and Lowest Housing Percentages from entire year range

# Extract max/min of Percent Affordable column

highest_affordable = df.nlargest(3, "Percent Affordable")
lowest_affordable = df.nsmallest(3, "Percent Affordable")

ct_coords = [41.60, -72.70] # the lat/long coordinates for the map of CT
geolocator = Nominatim(user_agent="geomap")

# This function uses geolocator to find lat/long of the corresponding town

def get_lat_long(town):
    location = geolocator.geocode(f"{town}, Connecticut")
    if location:
        return [location.latitude, location.longitude]
    else:
        return None, None


# We will assign folium markers to highest affordable perecentages

map = folium.Map(location=ct_coords, zoom_start=8)

for index, row in highest_affordable.iterrows():
    town_name = row['Town']
    percent_values = row['Percent Affordable']
    coords = get_lat_long(town_name)  # get_lat_long function applied
    if coords:
        folium.Marker(
            location=coords,
            popup=(f"<b>Highest Affordable Housing</b><br>"
                   f"Town: {town_name}<br>"
                   f"Percentage: {percent_values}%"),
            icon=folium.Icon(color='green', icon='arrow-up'),
        ).add_to(map)

# Assign markers for lowest affordable housing percentages

for index, row in lowest_affordable.iterrows():
    town_name = row['Town']
    percent_values = row['Percent Affordable']
    coords = get_lat_long(town_name)
    if coords:
        folium.Marker(
            location=coords,
            popup=(f"<b>Lowest Affordable Housing</b><br>"
                   f"Town: {town_name}<br>"
                   f"Percentage: {percent_values}%"),
            icon=folium.Icon(color='red', icon='arrow-down'),
        ).add_to(map)


st.subheader("Towns with Highest and Lowest Affordable Housing Percentages 2011-2023")
st_folium(map, width=800, height=600)
