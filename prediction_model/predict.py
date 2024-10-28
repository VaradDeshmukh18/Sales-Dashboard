import pandas as pd
import pickle
import streamlit as st

# Load the trained Random Forest model
with open('prediction_model/random_forest_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Get the expected feature names from the model
expected_feature_names = loaded_model.feature_names_in_

# Function to get user input and predict weekly sales
def predict_weekly_sales():
    # Streamlit widgets for user inputs
    holiday_flag = st.number_input("Enter Holiday Flag (0 or 1)", min_value=0, max_value=1)
    temperature = st.number_input("Enter Temperature (Fahrenheit)", format="%.2f")
    fuel_price = st.number_input("Enter Fuel Price", format="%.2f")
    cpi = st.number_input("Enter CPI", format="%.2f")
    unemployment = st.number_input("Enter Unemployment Rate", format="%.2f")
    Year = st.number_input("Enter Year", min_value=2000, max_value=2100)
    Month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12)
    Day = st.number_input("Enter Day", min_value=1, max_value=31)
    DayOfWeek = st.number_input("Enter Day of Week (1=Monday, 7=Sunday)", min_value=1, max_value=7)
    

    # Create a DataFrame from user input
    user_input = pd.DataFrame({
        'Holiday_Flag': [holiday_flag],
        'Temperature': [temperature],
        'Fuel_Price': [fuel_price],
        'CPI': [cpi],
        'Unemployment': [unemployment],
        'Year': [Year],
        'Month': [Month],
        'Day': [Day],
        'DayOfWeek': [DayOfWeek]
        
    })

    # Display the input DataFrame and expected feature names for debugging
    st.write("Input DataFrame:")
    st.write(user_input)
    st.write("Expected Feature Names:")
    st.write(expected_feature_names)

    # Predict weekly sales
    if st.button("Predict Weekly Sales"):
        try:
            predicted_sales = loaded_model.predict(user_input)
            st.write(f"Predicted Weekly Sales: ${predicted_sales[0]:,.2f}")
        except ValueError as e:
            st.error(f"Prediction failed: {str(e)}")

# Call the function to start the prediction process
if __name__ == "__main__":
    st.title("Weekly Sales Prediction")
    predict_weekly_sales()
