import streamlit as st
import plotly.express as px
import pandas as pd

# Load the dataset
data = pd.read_csv('dataset\Walmart_Sales.csv')

# Convert 'Date' column to datetime and extract relevant date information
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
data['Month'] = data['Date'].dt.month_name()
data['Quarter'] = data['Date'].dt.quarter
data['Year'] = data['Date'].dt.year

# Sidebar Filters (Store Selector, Holiday Flag, Date, Month, Quarter, Year)
st.sidebar.title("Filters")

# Store filter
store_options = data['Store'].unique().tolist()
selected_store = st.sidebar.selectbox("Select Store", options=["All"] + store_options)

# Holiday filter
holiday_flag_options = ["All", 0, 1]  # 0 = No Holiday, 1 = Holiday
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

# Function to filter data based on user selections
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

# Interactive state: Handle month click on treemap
if 'selected_month' not in st.session_state:
    st.session_state['selected_month'] = None

# Filter the data based on sidebar inputs
filtered_data = filter_data()

# Ensure there is data after filtering
if not filtered_data.empty:
    total_sales = filtered_data['Weekly_Sales'].sum()
    average_sales = filtered_data['Weekly_Sales'].mean()

    # Display total and average sales
    st.title("Sales Dashboard with Plotly (Interactive)")
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
    pivot_data = filtered_data.pivot_table(values='Weekly_Sales', index='Month', columns='Fuel_Price', aggfunc='mean')
    fig4 = px.imshow(pivot_data, labels=dict(x="Fuel Price", y="Month", color="Avg Sales"), title="Avg Sales by Month & Fuel Price")
    st.plotly_chart(fig4)

    # 5. Average Unemployment by CPI (Bar Chart)
    unemployment_cpi = filtered_data.groupby('CPI')['Unemployment'].mean().reset_index()
    fig5 = px.bar(unemployment_cpi, x='CPI', y='Unemployment', title="Avg Unemployment by CPI")
    st.plotly_chart(fig5)

    # 6. Average Weekly Sales by Month (Line Chart)
    monthly_sales = filtered_data.groupby('Month')['Weekly_Sales'].mean().reset_index()
    fig6 = px.line(monthly_sales, x='Month', y='Weekly_Sales', title="Average Weekly Sales by Month")
    st.plotly_chart(fig6)

else:
    st.error("No data available for the selected filters.")
