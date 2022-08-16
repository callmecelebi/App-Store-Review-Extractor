import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
from app_store_scraper import AppStore
from pprint import pprint
    
st.set_page_config(
    page_title="AppStore Reviews", 
    page_icon="✍🏼",
    layout="wide") # call page_config directly after the imports.

# mprof run streamlit run app.py

st.title('Extract App Reviews in the App Store')

st.subheader('Welcome to the App Store Reviews Extractor!')
data_load_state = st.text('Waiting for instructions...')

@st.cache
def getCountryCodes(path:str = 'data/country_codes.csv') -> set:
    try:
        df = pd.read_csv(path)
        return set(df['Code'].unique())
    except Exception as e:
        print(e)
        print("Error: Could not read data")
    
@st.cache
def getReviewsFromAPI(app_name, country: str = "us", how_many: int = 200) -> pd.DataFrame:
    try:
        appReviews = AppStore(country=country, app_name=app_name)
        appReviews.review(how_many=how_many)

        pprint(appReviews.reviews)
        df = pd.DataFrame.from_dict(appReviews.reviews)
        
        df['date'] = df['date'].dt.date
        
        # print(df.head(15))
        # pprint(appReviews.reviews_count)
        
        df = df.sort_values(by='date')
        
        return df
        pprint("Reviews scraped successfully.")
    except Exception as e:
        print(e)

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     data_load_state.text('Downloading data...done!')
     return df.to_csv().encode('utf-8')

appName = st.sidebar.text_input('Enter the app name:', 'minecraft')
howMany = st.sidebar.text_input('How many reviews you want to scrape:', '200')
countryCodes = getCountryCodes()
country = st.sidebar.selectbox('Choose a country please: ', countryCodes)

# Importing data
data_load_state = st.text('Loading data...')
# Importing data

reviewDf = getReviewsFromAPI(str(appName), country="us", how_many=int(howMany))

data_load_state.text('Loading data...done!')

st.subheader('Raw data')
rows = st.sidebar.text_input('How many rows you want to show in this page? (Automatically sorted by date)', '10')

st.write(reviewDf.head(int(rows)))
csv = convert_df(reviewDf)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',  )

