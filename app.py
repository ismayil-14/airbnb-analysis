import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import pymysql

myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='12345678',database = "cleaned_airbnb")

query = f""" select * from hotel """
hotel = pd.read_sql_query(query,myconnection)

query = f""" select * from host"""
host = pd.read_sql_query(query,myconnection)

query = f""" select * from review_score"""
review_score = pd.read_sql_query(query,myconnection)

query = f""" select * from availability """
availability = pd.read_sql_query(query,myconnection)

query = f""" select * from address"""
address = pd.read_sql_query(query,myconnection)

# Setting up page configuration
icon = Image.open("icon.png")
st.set_page_config(page_title= "Airbnb Data Visualization | By Mohamed Ismayil",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Mohamed Ismayil*!"""}
                  )

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview"], 
                           icons=["house","graph-up-arrow"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "25px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )



# HOME PAGE
if selected == "Home":
    # Title Image
    st.image("icon.png")
    st.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")
    st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit")
    st.markdown("## :blue[Overview] : To analyze Airbnb data using MySQL, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")

if selected == "Overview":
    col1,col2 = st.columns(2,gap='medium')

    with col1:
        query = f""" select property_type, avg(price) as avg_price from hotel group by property_type limit 10;"""
        df1 = pd.read_sql_query(query,myconnection)
        fig = px.pie(df1,
                        title='Average price for Top 10 Property_types',
                        names='property_type',
                        values='avg_price'
                    )
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
        query = f""" select room_type, avg(price) as avg_price , count(price) as count from hotel group by room_type"""
        df3 = pd.read_sql_query(query,myconnection)
        df3['label'] = df3.apply(lambda row: f"{row['room_type']} (Count: {row['count']}, Avg Price: ${row['avg_price']:.2f})", axis=1)

        # Create the pie chart
        fig = px.pie(df3,
                    title='Average Price and Count for Each Room Type',
                    names='label',
                    values='avg_price' 
                    )

        # Update the traces to include both value and label
        fig.update_traces(textposition='outside', textinfo='value+label')

        # Display the pie chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    query = f""" select country , count(hotel_id) as Count from address group by country;"""
    df2 = pd.read_sql_query(query,myconnection)
    fig = px.choropleth(df2,
                        title='Total Listings in each Country',
                        locations='country',
                        locationmode='country names',
                        color='Count',
                        color_continuous_scale=px.colors.sequential.Plasma
                        )
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("## Price Analysis")


 # CREATING COLUMNS
    col3,col4 = st.columns(2,gap='medium')
    
    with col3:
        # AVG PRICE IN COUNTRIES SCATTERGEO
        query = f""" select a.country as country , avg(b.price) as price from address as a left join hotel as b on a.hotel_id = b.hotel_id group by country;"""
        df3 = pd.read_sql_query(query,myconnection)
        fig = px.scatter_geo(data_frame=df3,
                                       locations='country',
                                       color= 'price', 
                                       hover_data=['price'],
                                       locationmode='country names',
                                       size='price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)
        
    with col4:
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        query = f""" select a.country as Country , avg(b.avail_365) as Availability from address as a left join availability as b on a.hotel_id = b.hotel_id group by country;"""
        df4 = pd.read_sql_query(query,myconnection)
        fig = px.scatter_geo(data_frame=df4,
                                       locations='Country',
                                       color= 'Availability', 
                                       hover_data=['Availability'],
                                       locationmode='country names',
                                       size='Availability',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)























































