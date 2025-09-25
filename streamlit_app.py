# Importing libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Setting the page title and layout
st.set_page_config(page_title="Produdct Analysis", page_icon="📦", layout="wide")
st.markdown("""
<style>
    /* 1. General page background */
    .stApp {
        background-color: #f0f2f6; /* Light gray background for the main content */
    }

    /* 2. Target the sidebar (Streamlit's main sidebar div class) */
    [data-testid="stSidebar"] {
        background-color: #0c1a2c; /* Dark blue/almost black for sidebar */
        color: white; /* Ensure text is white */
        /* Optionally change font for the sidebar */
        font-family: Arial, sans-serif; 
    }
    
    /* 3. Ensure all titles/text in the sidebar are white */
    [data-testid="stSidebar"] .stButton > button, 
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* 4. Improve the look of st.metric containers */
    [data-testid="stMetric"] {
        background-color: white; /* White background for metric boxes */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    }
</style>
""", unsafe_allow_html=True)

# Function for upload the data by type
@st.cache_data
def load_data(dataset):
    if dataset.type == "text/csv":
        df = pd.read_csv(dataset)
    elif dataset.type == "application/json":
        df = pd.read_json(dataset)
    else:
        df = pd.read_excel(dataset)
    return df

# Functions for save filter when they're used
def category_filter():
    st.session_state["categories_filter"] = st.session_state.get("multiselect_categories", [])

def price_filter():
    st.session_state["prices_filter"] = st.session_state.get("slider_prices", [])

# Page tabs or windows
tab1, tab2 = st.tabs(["Presentation", "Dashboard"])

# Tab of presentation
with tab1:
    st.title("Welcome!")
    st.header("This is the product app web where you can see the company products state")
    st.write("Above you can choose the dashboard, or see the raw data if you're interest (However, you can also see it in the dashboard)")

# Tab of dashboard
with tab2:
    # Main image of the app
    st.sidebar.image("Gemini_Generated_Image.png", width=200)
    
    # Title in the sidebar
    st.sidebar.title("Product Analyzer")
    
    # Text bellow the title from the sidebar
    st.sidebar.subheader("Dasboard of the products of the company")
    
    # Data uploader, so the user can choose the file (the columns must match)
    dataset = st.sidebar.file_uploader("Select the dataset", type=["txt", "csv", "xlsx", "json"])
    
    # Operations when the data is upload
    if dataset:
        # Try the next codes if an error doesn't occur
        try:
            # Load data function
            df = load_data(dataset)
    
            # Loading the dashboard
            with st.spinner("Building dashboard"):
    
                # Start the saved filters
                if "categories_filter" not in st.session_state:
                    st.session_state = df["category"].unique()
                if "prices_filter" not in st.session_state:
                    st.session_state = (df["price"].min(), df["price"].max())
                
                # A select box for filter by category
                categories = st.sidebar.multiselect(
                    "Select the category of products you want to see", 
                    options=df["category"].unique(), 
                    default=df["category"].unique(),
                    key="multiselect_categories"
                )
            
                # A slider for choose a range of price
                prices = st.sidebar.slider(
                    "Select a range of prices of products", 
                    df["price"].min(), 
                    df["price"].max(), 
                    (df["price"].min(), df["price"].max()),
                    key="slider_prices"
                )
        
                # Apply filters by the user options
                data = df.copy()
                data = data[data["category"].isin(categories)]
                data = data[(data["price"] >= prices[0]) & (data["price"] <= prices[1])]
            
                # Title of the page
                st.title("Product Analysis Dashboard")
            
                # Text bellow the title
                st.write("Summary of the situation of the company")
            
                # Containers for the metrics
                col1, col2, col3 = st.columns(3)
            
                # Metrics
                col1.metric("Total Sales", f"{data['sales'].sum().round():,}")
                col2.metric("Average Rating", data["rating"].mean().round(2))
                col3.metric("Number of Unique products", data["product_id"].nunique())
        
                # Divide two sections of the page
                st.divider()
            
                # Creating a bar chart with streamlit
                st.bar_chart(data, x="category", y="sales")
            
                # Creating a scatter plot using plotly
                fig_scatter = px.scatter(data, x="units_sold", y="price", title="Relation between price and units sold")
                st.plotly_chart(fig_scatter)
            
                # Simply showing dataframe in the app
                with st.expander("Raw data"):
                    st.subheader("The entire dataframe")
                    st.dataframe(data)
                    st.subheader("Download the dataset!")
                    st.write("Warning: If you want the full dataset, restart the filters or you'll get incomplete data depending of the choosed filters")
                    st.download_button("Download dataset", data.to_csv(index=False), file_name="dataset.csv", mime="text/csv")

        # Exception when an error occur
        except Exception as e:
            st.error("You didn't provide the correct dataset. Bring the correct dataset provided to you")

    # Message if data doesn't upload
    else:
        st.info("Please upload a dataset to begin")