import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from data_preprocessing import preprocess_data # Import the created Data_Preprocesing.py file 

df = pd.read_csv("Affordable_Housing_by_Town_2011-2023_2024.csv")

df = preprocess_data(df) # data pre-procesing file will update DataFrame automatically


st.title("CT Affordable Housing Impact")

# Interactive Widgets

with st.sidebar:
    county_filter = st.sidebar.multiselect("Select County(s):", options=df['County'].unique(), default=df['County'].unique()) # Can select single/multiple counties for analysis
    year_filter = st.sidebar.slider("Select Year Range:", int(df['Year'].min()), int(df['Year'].max()), (2020, 2022)) # Implemented slider for users to select specific year ranges
    filtered_df = df[(df['County'].isin(county_filter)) & (df['Year'].between(year_filter[0], year_filter[1]))]
    columns_for_radio = df.columns[2:7] # Ct programs listed as radio buttons 
    selected_column = st.radio("Select a column for analysis:", options=columns_for_radio) 

# Line chart

st.subheader(f"{selected_column} Over Time")  # The line chart will update automatically when a housing program is selected

aggregated_df = filtered_df.groupby(['Year', 'County'], as_index=False).agg({selected_column: 'mean'}) # Ensures avg impact for each county is plotted 

fig = px.line(
    aggregated_df,  # Use the aggregated data created
    x='Year',
    y=selected_column,
    color='County',  
    markers=True,
    title=f"{selected_column} by County Over Time",
    labels={"Year": "Year", selected_column: selected_column},
    hover_data=['County', 'Year', selected_column]
)

fig.update_layout(
    width=800,
    height=400,
    legend_title="County",  
    title_x=0.5
)

# Display the plot
st.plotly_chart(fig)
    
# A table is also implemented to display the percent of affordable housing for clarity

# Can filter based on the year range chosen from the slider

st.subheader("Towns with Highest and Lowest Affordable Housing Percentages")
highest = filtered_df.loc[filtered_df.groupby('Year')['Percent Affordable'].idxmax()]
lowest = filtered_df.loc[filtered_df.groupby('Year')['Percent Affordable'].idxmin()]

st.write("### Highest Percent Affordable")
st.table(highest[['Year', 'Town', 'County','Percent Affordable']])
st.write("### Lowest Percent Affordable")
st.table(lowest[['Year', 'Town', 'County', 'Percent Affordable']])

# Will plot Folium map of Highest and Lowest Housing Percentages

# Extract max/min of Percent Affordable

highest_affordable = filtered_df.loc[filtered_df['Percent Affordable'].idxmax()]
lowest_affordable = filtered_df.loc[filtered_df['Percent Affordable'].idxmin()]

ct_coords = [41.60, -72.70] # the lat/long coordinates for the map of CT
geolocator = Nominatim(user_agent="geomap")

# This function uses geolocator to find lat/long of the corresponding town

def get_lat_long(town):
    location = geolocator.geocode(f"{town}, Connecticut")
    if location:
        return [location.latitude, location.longitude]
    else:
        return None, None

# Assign values to corresponding towns

high_loc = get_lat_long(highest_affordable['Town'])
low_loc = get_lat_long(lowest_affordable['Town'])

# We will assign folium markers 

m = folium.Map(location=ct_coords, zoom_start=8)

folium.Marker(
    location=high_loc,
    popup=(f"<b>Highest Affordable Housing</b><br>"
           f"<b>Town:</b> {highest_affordable['Town']}<br>" # To ensure name of city for highest affordable is displayed in marker
           f"<b>County:</b> {highest_affordable['County']}<br>" # Same with corresponding county
           f"<b>Percentage:</b> {highest_affordable['Percent Affordable']}%"), # To ensure assigned value pops up as well
    icon=folium.Icon(color='green', icon='arrow-up'),
).add_to(m)

folium.Marker(
    location=low_loc,
    popup=(f"<b>Lowest Affordable Housing</b><br>"
           f"<b>Town:</b> {lowest_affordable['Town']}<br>" # To ensure name of city for lowest affordable is displayed in marker
           f"<b>County:</b> {lowest_affordable['County']}<br>" # Same with corresponding County
           f"<b>Percentage:</b> {lowest_affordable['Percent Affordable']}%"), # To ensure assigned value pops up in marker as well
    icon=folium.Icon(color='red', icon='arrow-down'),
).add_to(m)

st.subheader("Towns with Highest and Lowest Affordable Housing Percentages")
st_folium(m, width=800, height=600)
