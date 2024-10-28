import streamlit as st
import plotly.express as px
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Google Sheets Authentication
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(os.getenv("json_credentials"), scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("google_sheet_id")).sheet1
except Exception as e:
    st.error(f"Error in Google Sheets connection: {e}")
    st.stop()

# Load data from Google Sheets and handle expected headers
try:
    expected_headers = ["Store", "Date", "Weekly_Sales", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI", "Unemployment"]
    data = pd.DataFrame(sheet.get_all_records(expected_headers=expected_headers))
except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")
    st.stop()

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce', dayfirst=True)

# Drop rows with invalid dates
data = data.dropna(subset=['Date'])

# Create 'Month', 'Quarter', and 'Year' columns
data['Month'] = data['Date'].dt.month_name()
data['Quarter'] = data['Date'].dt.quarter
data['Year'] = data['Date'].dt.year

# Sidebar Filters
st.sidebar.title("Filters")

# Store filter
store_options = data['Store'].unique().tolist()
selected_store = st.sidebar.selectbox("Select Store", options=["All"] + store_options)

# Holiday filter
holiday_flag_options = ["All", 0, 1]
selected_holiday = st.sidebar.selectbox("Holiday Flag", options=holiday_flag_options)

# Date filter
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())

# Month filter
month_options = data['Month'].unique().tolist()
selected_month = st.sidebar.multiselect("Select Month", options=month_options, default=month_options)

# Quarter filter
quarter_options = [1, 2, 3, 4]
selected_quarter = st.sidebar.multiselect("Select Quarter", options=quarter_options, default=quarter_options)

# Year filter
year_options = data['Year'].unique().tolist()
selected_year = st.sidebar.multiselect("Select Year", options=year_options, default=year_options)

# Function to filter data
def filter_data():
    filtered_data = data.copy()

    # Filter by store
    if selected_store != "All":
        filtered_data = filtered_data[filtered_data['Store'] == selected_store]

    # Filter by holiday flag
    if selected_holiday != "All":
        filtered_data = filtered_data[filtered_data['Holiday_Flag'] == selected_holiday]

    # Filter by date range
    filtered_data = filtered_data[(filtered_data['Date'] >= pd.to_datetime(start_date)) & 
                                  (filtered_data['Date'] <= pd.to_datetime(end_date))]

    # Filter by month
    if selected_month:
        filtered_data = filtered_data[filtered_data['Month'].isin(selected_month)]

    # Filter by quarter
    if selected_quarter:
        filtered_data = filtered_data[filtered_data['Quarter'].isin(selected_quarter)]

    # Filter by year
    if selected_year:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_year)]

    return filtered_data

# Filter the data
filtered_data = filter_data()

# Ensure there is data after filtering
if not filtered_data.empty:
    total_sales = filtered_data['Weekly_Sales'].sum()
    average_sales = filtered_data['Weekly_Sales'].mean()

    st.title("Walmart Sales Dashboard")
    st.markdown(f"### Total Sales: ${total_sales:,.2f}")
    st.markdown(f"### Average Sales: ${average_sales:,.2f}")

    # 1. Median Weekly Sales by Holiday (Pie Chart)
    holiday_sales = filtered_data.groupby('Holiday_Flag')['Weekly_Sales'].median().reset_index()
    holiday_sales['Holiday'] = holiday_sales['Holiday_Flag'].map({0: 'False', 1: 'True'})
    fig1 = px.pie(holiday_sales, values='Weekly_Sales', names='Holiday', title="Median Weekly Sales by Holiday")
    st.plotly_chart(fig1)

    # 2. Weekly Sales by Quarter and Temperature (Scatter Plot)
    fig2 = px.scatter(filtered_data, x='Temperature', y='Weekly_Sales', color='Quarter', 
                      title="Weekly Sales by Quarter & Temperature", labels={'Quarter': 'Quarter'})
    st.plotly_chart(fig2)

    # 3. Median Weekly Sales by Store (Donut Chart)
    store_sales = filtered_data.groupby('Store')['Weekly_Sales'].median().reset_index()
    fig3 = px.pie(store_sales, values='Weekly_Sales', names='Store', hole=.3, title="Median Weekly Sales by Store")
    st.plotly_chart(fig3)

    # 4. Average Sales by Month and Fuel Price (Heatmap)
    pivot_data = filtered_data.pivot_table(values='Weekly_Sales', index='Month', columns='Fuel_Price', aggfunc='mean', fill_value=0)
    fig4 = px.imshow(pivot_data, labels=dict(x="Fuel Price", y="Month", color="Avg Sales"), title="Avg Sales by Month & Fuel Price")
    st.plotly_chart(fig4)

    # 5. Average Unemployment by CPI (Bar Chart)
    unemployment_cpi = filtered_data.groupby('CPI').agg({'Unemployment': 'mean'}).reset_index()
    fig5 = px.bar(unemployment_cpi, x='CPI', y='Unemployment', title="Avg Unemployment by CPI")
    st.plotly_chart(fig5)

    # 6. Average Weekly Sales by Month (Line Chart)
    monthly_sales = filtered_data.groupby('Month')['Weekly_Sales'].mean().reindex(
        ['January', 'February', 'March', 'April', 'May', 'June', 
         'July', 'August', 'September', 'October', 'November', 'December']).reset_index()
    fig6 = px.line(monthly_sales, x='Month', y='Weekly_Sales', title="Average Weekly Sales by Month")
    st.plotly_chart(fig6)

else:
    st.error("No data available for the selected filters.")

# --- CRUD Operations ---
st.sidebar.title("CRUD Operations")

# Options for CRUD Operations
crud_options = ['Show Dataset', 'Add Row', 'Update Row', 'Delete Row']
selected_crud = st.sidebar.selectbox("Select CRUD Operation", options=crud_options)

# Show Dataset
if selected_crud == 'Show Dataset':
    st.write("### Current Dataset")
    st.dataframe(data)

# Add Row
if selected_crud == 'Add Row':
    st.write("### Add New Row")
    new_row = {}
    for col in expected_headers:  # Only loop through the original headers
        if col == "Date":
            new_row[col] = st.date_input(f"Enter {col}").strftime('%Y-%m-%d')
        else:
            new_row[col] = st.text_input(f"Enter {col}")

    if st.button("Add Row"):
        # Append the new row to Google Sheets (only original headers)
        sheet.append_row(list(new_row.values()))
        st.success("Row added successfully.")
        st.experimental_set_query_params()


# Get the header (assuming it's in the first row of the sheet)
header = sheet.row_values(1)

# Update Row
if selected_crud == 'Update Row':
    st.write("### Update Row")
    
    row_number = st.number_input("Enter the row number to update", min_value=2, step=1)
    
    row_data = sheet.row_values(row_number)
    st.write(f"Current Data for Row {row_number}: {row_data}")

    updated_values = {}
    
    # Display text inputs for each header and pre-fill current values from row_data
    for idx, key in enumerate(header):
        updated_value = st.text_input(f"Update {key}", row_data[idx] if idx < len(row_data) else "")
        updated_values[key] = updated_value

    if st.button("Update Row"):
        try:
            # Ensure row_data has enough elements, update or append new values
            for idx, key in enumerate(header):
                if idx < len(row_data):
                    row_data[idx] = updated_values[key]
                else:
                    row_data.append(updated_values[key])
            
            # Update the row in Google Sheet (adjust the range 'A{row_number}:I{row_number}' if needed)
            sheet.update(f'A{row_number}:I{row_number}', [row_data])  
            st.success(f"Row {row_number} updated successfully.")
        except Exception as e:
            st.error(f"Error updating row: {e}")
    st.experimental_set_query_params()



# Delete Row
if selected_crud == 'Delete Row':
    st.write("### Delete Row")
    row_number = st.number_input("Enter the row number to delete", min_value=2, step=1)
    
    if st.button("Delete Row"):
        try:
            sheet.delete_rows(row_number)  # Use delete_rows instead of delete_row
            st.success(f"Row {row_number} deleted successfully.")
        except Exception as e:
            st.error(f"Error deleting row: {e}")
    st.experimental_set_query_params()

# Add a button for prediction
if st.sidebar.button("Predict"):
    try:
        exec(open("predict.py").read())  # Execute the uploaded predict.py file
    except Exception as e:
        st.error(f"Error in prediction: {e}")
