# Walmart Sales Dashboard

A comprehensive dashboard built with Streamlit that visualizes and analyzes Walmart sales data from Google Sheets, featuring interactive filters, multiple visualization types, and CRUD operations.

## Features

### Data Visualization
- Total and average sales metrics
- Multiple interactive charts:
  - Median weekly sales by holiday (Pie Chart)
  - Weekly sales by quarter and temperature (Scatter Plot)
  - Median weekly sales by store (Donut Chart)
  - Average sales by month and fuel price (Heatmap)
  - Average unemployment by CPI (Bar Chart)
  - Average weekly sales by month (Line Chart)

### Filtering Capabilities
- Store selection
- Holiday flag filter
- Date range selection
- Month filter (multiple selection)
- Quarter filter (multiple selection)
- Year filter (multiple selection)

### CRUD Operations
- View complete dataset
- Add new data rows
- Update existing rows
- Delete rows from the dataset

## Prerequisites

- Python 3.7+
- Google Cloud Platform account
- Google Sheets API enabled
- Service account credentials

## Required Python Packages

```bash
streamlit
plotly
pandas
gspread
google-auth
python-dotenv
datetime
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd walmart-sales-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
json_credentials=path/to/your/credentials.json
google_sheet_id=your_google_sheet_id
```

## Google Sheets Setup

1. Create a new Google Sheet with the following headers:
   - Store
   - Date
   - Weekly_Sales
   - Holiday_Flag
   - Temperature
   - Fuel_Price
   - CPI
   - Unemployment

2. Share the sheet with the service account email (found in your credentials.json)

## Running the Application

1. Navigate to the project directory:
```bash
cd walmart-sales-dashboard
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Access the dashboard in your web browser at `http://localhost:8501`

## Usage

### Filtering Data
1. Use the sidebar filters to select:
   - Specific stores or all stores
   - Holiday/non-holiday periods
   - Date ranges
   - Specific months
   - Quarters
   - Years

### Managing Data
1. Select CRUD Operations from the sidebar:
   - View the complete dataset
   - Add new records with the data entry form
   - Update existing records by specifying row number
   - Delete records by row number

### Viewing Visualizations
- All charts automatically update based on the selected filters
- Hover over charts for detailed information
- Click and drag on charts to zoom
- Use the plot toolbar to download charts, pan, or reset the view

## Data Structure

The dashboard expects the following data structure in Google Sheets:

| Column         | Type      | Description                               |
|---------------|-----------|-------------------------------------------|
| Store         | Integer   | Store identifier                          |
| Date          | Date      | Date of sales record                      |
| Weekly_Sales  | Float     | Weekly sales amount                       |
| Holiday_Flag  | Integer   | 1 for holiday week, 0 for non-holiday     |
| Temperature   | Float     | Average temperature for the week          |
| Fuel_Price    | Float     | Average fuel price for the week          |
| CPI           | Float     | Consumer Price Index                      |
| Unemployment  | Float     | Unemployment rate                         |

## Error Handling

The dashboard includes error handling for:
- Google Sheets connection issues
- Invalid data formats
- Missing or incorrect data
- CRUD operation failures

## Security Considerations

- Keep your `.env` file secure and never commit it to version control
- Store your Google Cloud credentials securely
- Implement proper access controls on your Google Sheet
- Consider implementing user authentication for the dashboard



