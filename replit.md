# Stock Analysis Tool

## Overview

This is a Streamlit-based stock analysis application that provides comprehensive financial data and analysis for any stock symbol. The application uses Yahoo Finance data to display stock information with interactive charts and financial metrics.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - Python web framework for data applications
- **UI Components**: Streamlit native components with sidebar navigation
- **Visualization**: Plotly for interactive charts and graphs
- **Layout**: Wide layout configuration for better data presentation

### Backend Architecture
- **Data Source**: Yahoo Finance API via yfinance library
- **Data Processing**: Pandas for data manipulation and NumPy for numerical operations
- **Real-time Data**: Direct API calls to Yahoo Finance for current stock data
- **No Database**: Application fetches data on-demand without persistent storage

## Key Components

### Data Acquisition
- **yfinance Library**: Primary data source for stock information
- **Real-time Fetching**: Stock data retrieved on user request
- **Historical Data**: Supports multiple time periods (1 month to 5 years)

### User Interface
- **Sidebar Controls**: Stock symbol input and time period selection
- **Main Dashboard**: Display area for charts and financial metrics
- **Interactive Elements**: Analyze button to trigger data fetching

### Visualization
- **Plotly Integration**: Interactive charts for stock price movements
- **Multiple Chart Types**: Support for various financial visualizations
- **Responsive Design**: Charts adapt to different screen sizes

### Data Processing
- **Currency Formatting**: Utility function for displaying financial figures
- **Data Validation**: Input validation for stock symbols
- **Error Handling**: Graceful handling of invalid stock symbols or API errors

## Data Flow

1. **User Input**: User enters stock symbol and selects time period
2. **Data Fetch**: Application calls Yahoo Finance API via yfinance
3. **Data Processing**: Raw data processed using Pandas/NumPy
4. **Visualization**: Processed data rendered using Plotly charts
5. **Display**: Results presented in Streamlit interface

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **yfinance**: Yahoo Finance data access
- **plotly**: Interactive charting library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### Data Sources
- **Yahoo Finance API**: Primary source for stock market data
- **Real-time Market Data**: Current and historical stock prices

## Deployment Strategy

### Local Development
- **Python Environment**: Requires Python 3.7+ with pip package management
- **Streamlit Server**: Local development server via `streamlit run app.py`
- **Dependencies**: All libraries installable via pip

### Production Deployment
- **Replit Compatible**: Designed to run on Replit platform
- **Cloud Deployment**: Can be deployed on Streamlit Cloud, Heroku, or similar platforms
- **No Database Required**: Stateless application with external data dependencies

### Configuration
- **Page Settings**: Wide layout with custom title and icon
- **Default Values**: AAPL stock with 1-year period as defaults
- **Responsive Design**: Adapts to different screen sizes

## Changelog

- June 29, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.