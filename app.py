import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Set page configuration
st.set_page_config(
    page_title="Stock Analysis Tool",
    page_icon="📈",
    layout="wide"
)

# Main title
st.title("📈 Stock Analysis Tool")
st.markdown("Get comprehensive financial data and analysis for any stock symbol")

# Sidebar for stock input and time period selection
st.sidebar.header("Stock Selection")
stock_symbol = st.sidebar.text_input(
    "Enter Stock Symbol (e.g., AAPL, GOOGL, TSLA)",
    value="AAPL",
    help="Enter a valid stock ticker symbol"
).upper()

# Time period selection
time_periods = {
    "1 Month": "1mo",
    "3 Months": "3mo", 
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y"
}

selected_period = st.sidebar.selectbox(
    "Select Time Period",
    options=list(time_periods.keys()),
    index=3  # Default to 1 Year
)

# Analyze button
analyze_button = st.sidebar.button("Analyze Stock", type="primary")

def format_currency(value):
    """Format large numbers as currency with appropriate suffixes"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    if abs(value) >= 1e12:
        return f"${value/1e12:.2f}T"
    elif abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.2f}"

def format_number(value):
    """Format large numbers with appropriate suffixes"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    if abs(value) >= 1e9:
        return f"{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.2f}K"
    else:
        return f"{value:,.2f}"

def get_stock_data(symbol, period):
    """Fetch stock data from Yahoo Finance"""
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get stock info
        info = ticker.info
        
        # Get historical data
        hist_data = ticker.history(period=time_periods[period])
        
        if hist_data.empty:
            return None, None, "No data found for this symbol"
        
        return info, hist_data, None
        
    except Exception as e:
        return None, None, f"Error fetching data: {str(e)}"

def display_company_info(info):
    """Display company information"""
    st.subheader("Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Country:** {info.get('country', 'N/A')}")
    
    with col2:
        st.write(f"**Website:** {info.get('website', 'N/A')}")
        st.write(f"**Employees:** {format_number(info.get('fullTimeEmployees', 'N/A'))}")
        st.write(f"**Exchange:** {info.get('exchange', 'N/A')}")
        st.write(f"**Currency:** {info.get('currency', 'N/A')}")
    
    # Business summary
    if info.get('longBusinessSummary'):
        st.write("**Business Summary:**")
        st.write(info['longBusinessSummary'])

def display_key_metrics(info):
    """Display key financial metrics in a table"""
    st.subheader("Key Financial Metrics")
    
    # Create metrics data
    current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
    previous_close = info.get('previousClose', 'N/A')
    
    # Calculate price change
    if current_price != 'N/A' and previous_close != 'N/A':
        price_change = current_price - previous_close
        price_change_pct = (price_change / previous_close) * 100
    else:
        price_change = 'N/A'
        price_change_pct = 'N/A'
    
    metrics_data = {
        'Metric': [
            'Current Price',
            'Previous Close',
            'Price Change',
            'Price Change (%)',
            'Day Range',
            '52 Week Range',
            'Volume',
            'Average Volume',
            'Market Cap',
            'Enterprise Value',
            'P/E Ratio',
            'Forward P/E',
            'Price to Book',
            'Price to Sales',
            'Dividend Yield',
            'Beta',
            'EPS (TTM)',
            'Revenue (TTM)',
            'Profit Margin',
            'Operating Margin'
        ],
        'Value': [
            f"${current_price:.2f}" if current_price != 'N/A' else 'N/A',
            f"${previous_close:.2f}" if previous_close != 'N/A' else 'N/A',
            f"${price_change:.2f}" if price_change != 'N/A' else 'N/A',
            f"{price_change_pct:.2f}%" if price_change_pct != 'N/A' else 'N/A',
            f"${info.get('dayLow', 'N/A')} - ${info.get('dayHigh', 'N/A')}" if info.get('dayLow') and info.get('dayHigh') else 'N/A',
            f"${info.get('fiftyTwoWeekLow', 'N/A')} - ${info.get('fiftyTwoWeekHigh', 'N/A')}" if info.get('fiftyTwoWeekLow') and info.get('fiftyTwoWeekHigh') else 'N/A',
            format_number(info.get('volume', 'N/A')),
            format_number(info.get('averageVolume', 'N/A')),
            format_currency(info.get('marketCap', 'N/A')),
            format_currency(info.get('enterpriseValue', 'N/A')),
            f"{info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else 'N/A',
            f"{info.get('forwardPE', 'N/A'):.2f}" if info.get('forwardPE') else 'N/A',
            f"{info.get('priceToBook', 'N/A'):.2f}" if info.get('priceToBook') else 'N/A',
            f"{info.get('priceToSalesTrailing12Months', 'N/A'):.2f}" if info.get('priceToSalesTrailing12Months') else 'N/A',
            f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else 'N/A',
            f"{info.get('beta', 'N/A'):.2f}" if info.get('beta') else 'N/A',
            f"${info.get('trailingEps', 'N/A'):.2f}" if info.get('trailingEps') else 'N/A',
            format_currency(info.get('totalRevenue', 'N/A')),
            f"{info.get('profitMargins', 0) * 100:.2f}%" if info.get('profitMargins') else 'N/A',
            f"{info.get('operatingMargins', 0) * 100:.2f}%" if info.get('operatingMargins') else 'N/A'
        ]
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    
    # Display in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(metrics_df.iloc[:10], hide_index=True, use_container_width=True)
    
    with col2:
        st.dataframe(metrics_df.iloc[10:], hide_index=True, use_container_width=True)

def create_price_chart(hist_data, symbol):
    """Create interactive price chart"""
    st.subheader(f"Price Chart - {symbol}")
    
    # Create candlestick chart
    fig = go.Figure(data=go.Candlestick(
        x=hist_data.index,
        open=hist_data['Open'],
        high=hist_data['High'],
        low=hist_data['Low'],
        close=hist_data['Close'],
        name=symbol
    ))
    
    fig.update_layout(
        title=f"{symbol} Stock Price",
        yaxis_title="Price ($)",
        xaxis_title="Date",
        height=600,
        showlegend=False,
        xaxis_rangeslider_visible=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_volume_chart(hist_data, symbol):
    """Create volume chart"""
    st.subheader(f"Trading Volume - {symbol}")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=hist_data.index,
        y=hist_data['Volume'],
        name='Volume',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title=f"{symbol} Trading Volume",
        yaxis_title="Volume",
        xaxis_title="Date",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_moving_averages_chart(hist_data, symbol):
    """Create moving averages chart"""
    st.subheader(f"Moving Averages - {symbol}")
    
    # Calculate moving averages
    hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
    hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
    
    fig = go.Figure()
    
    # Add closing price
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue')
    ))
    
    # Add moving averages
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['MA20'],
        mode='lines',
        name='20-day MA',
        line=dict(color='orange')
    ))
    
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['MA50'],
        mode='lines',
        name='50-day MA',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title=f"{symbol} Price with Moving Averages",
        yaxis_title="Price ($)",
        xaxis_title="Date",
        height=500,
        legend=dict(x=0, y=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Main application logic
if stock_symbol and (analyze_button or 'last_symbol' not in st.session_state or st.session_state.last_symbol != stock_symbol):
    # Store the last analyzed symbol
    st.session_state.last_symbol = stock_symbol
    
    with st.spinner(f"Fetching data for {stock_symbol}..."):
        info, hist_data, error = get_stock_data(stock_symbol, selected_period)
    
    if error:
        st.error(f"❌ {error}")
        st.info("Please check the stock symbol and try again. Make sure it's a valid ticker symbol (e.g., AAPL, GOOGL, TSLA).")
    
    elif info and hist_data is not None:
        # Display success message
        st.success(f"✅ Successfully loaded data for {stock_symbol}")
        
        # Display company information
        display_company_info(info)
        
        st.divider()
        
        # Display key metrics
        display_key_metrics(info)
        
        st.divider()
        
        # Create charts in tabs
        tab1, tab2, tab3 = st.tabs(["📈 Price Chart", "📊 Volume", "📉 Moving Averages"])
        
        with tab1:
            create_price_chart(hist_data, stock_symbol)
        
        with tab2:
            create_volume_chart(hist_data, stock_symbol)
        
        with tab3:
            create_moving_averages_chart(hist_data, stock_symbol)
        
        # Display raw data option
        st.divider()
        
        if st.checkbox("Show Raw Historical Data"):
            st.subheader("Historical Data")
            st.dataframe(hist_data.round(2), use_container_width=True)
            
            # Download option
            csv_data = hist_data.to_csv()
            st.download_button(
                label="Download Historical Data as CSV",
                data=csv_data,
                file_name=f"{stock_symbol}_historical_data.csv",
                mime="text/csv"
            )

else:
    # Display welcome message
    st.info("👈 Enter a stock symbol in the sidebar and click 'Analyze Stock' to get started!")
    
    # Display sample symbols
    st.subheader("Popular Stock Symbols")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**Technology:**")
        st.write("• AAPL (Apple)")
        st.write("• GOOGL (Alphabet)")
        st.write("• MSFT (Microsoft)")
        st.write("• TSLA (Tesla)")
    
    with col2:
        st.write("**Finance:**")
        st.write("• JPM (JPMorgan)")
        st.write("• BAC (Bank of America)")
        st.write("• WFC (Wells Fargo)")
        st.write("• GS (Goldman Sachs)")
    
    with col3:
        st.write("**Healthcare:**")
        st.write("• JNJ (Johnson & Johnson)")
        st.write("• PFE (Pfizer)")
        st.write("• UNH (UnitedHealth)")
        st.write("• ABBV (AbbVie)")
    
    with col4:
        st.write("**Consumer:**")
        st.write("• AMZN (Amazon)")
        st.write("• WMT (Walmart)")
        st.write("• KO (Coca-Cola)")
        st.write("• PG (Procter & Gamble)")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        📊 Stock Analysis Tool | Data provided by Yahoo Finance
    </div>
    """, 
    unsafe_allow_html=True
)
