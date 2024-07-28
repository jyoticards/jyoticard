import streamlit as st
import pandas as pd
import os

logo_path = 'jyoti logo-1.png'

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    .title {
        font-size: 2.5em;
        color: #4e8cff;
        font-weight: bold;
        text-align: center;
        margin-top: 0;
        padding-top: 0;
    }
    .input {
        font-size: 1.25em;
        color: #333;
    }
    .result {
        font-size: 1.25em;
        color: #333;
        font-weight: bold;
        text-align: center;
    }
    .footer {
        font-size: 1em;
        color: #888;
        text-align: center;
        margin-top: 2em;
    }
    .in-stock {
        color: green;
        background-color: #d4f8d4;
        padding: 10px;
        border-radius: 5px;
    }
    .out-of-stock {
        color: red;
        background-color: #f8d4d4;
        padding: 10px;
        border-radius: 5px;
    }
    .low-stock {
        color: orange;
        background-color: #fff2cc;
        padding: 10px;
        border-radius: 5px;
    }
    .highlight-green {
        font-size: 1.25em;
        font-weight: bold;
        color: #ffffff;
        background-color: #28a745;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-top: 1em;
    }
    .highlight-yellow {
        font-size: 1.25em;
        font-weight: bold;
        color: #ffffff;
        background-color: #ffc107;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-top: 1em;
    }
    .highlight-red {
        font-size: 1.25em;
        font-weight: bold;
        color: #ffffff;
        background-color: #dc3545;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-top: 1em;
    }
    .marquee {
        font-size: 1.25em;
        font-weight: bold;
        background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);
        -webkit-background-clip: text;
        color: transparent;
        animation: marquee 10s linear infinite;
    }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add the marquee line
st.markdown('<div class="marquee">Offer of the Day - 5% off</div>', unsafe_allow_html=True)

# Load the Excel file
file_path = 'STK SUMMARY NEW.XLSX'
df = pd.read_excel(file_path)

# Remove rows 1 to 8
df_cleaned = df.iloc[8:].reset_index(drop=True)

# Rename the columns
df_cleaned.columns = ['ITEM NO.', 'Quantity']

# Process the ITEM NO. column
df_cleaned['ITEM NO.'] = df_cleaned['ITEM NO.'].apply(lambda x: x.split()[0] if isinstance(x, str) and x.split()[0].isdigit() else x)

# Process the Quantity column
df_cleaned['Quantity'] = df_cleaned['Quantity'].astype(str).str.replace(' pcs', '').astype(float) * 100

cleaned_df = df_cleaned

# Load the alternative list data
alternative_list_file = 'ALTERNATIVE LIST.xlsx'
alternative_df = pd.read_excel(alternative_list_file)

# Strip any extra spaces from column names
alternative_df.columns = alternative_df.columns.str.strip()

# Ensure ITEM NO. columns are of the same type
cleaned_df['ITEM NO.'] = cleaned_df['ITEM NO.'].astype(str)
alternative_df['ITEM NO.'] = alternative_df['ITEM NO.'].astype(str)

# Get the list of ITEM NO. values and add an empty option
item_no_list = [''] + cleaned_df['ITEM NO.'].tolist()

# Streamlit app
st.image(logo_path, width=200)  # Display the logo
st.markdown('<h1 class="title">Jyoti Cards Stock Status</h1>', unsafe_allow_html=True)

# Dropdown for ITEM NO.
item_no = st.selectbox('Select ITEM NO.', item_no_list, index=0)

if item_no:
    # Check if ITEM NO. exists in cleaned data
    item_row = cleaned_df[cleaned_df['ITEM NO.'] == item_no]
    
    if not item_row.empty:
        quantity = item_row['Quantity'].values[0]
    else:
        quantity = None
    
    # Get the corresponding row in the alternative list
    alt_row = alternative_df[alternative_df['ITEM NO.'] == item_no]
    
    if not alt_row.empty:
        condition_value = alt_row['CONDITION'].values[0]
        rate = alt_row['RATE'].values[0]
        item_type = alt_row['ITEM TYPE'].values[0]
        a = alt_row['A'].values[0]
        b = alt_row['B'].values[0]
        c = alt_row['C'].values[0]
    else:
        st.markdown('<p class="result">ITEM NO. not available</p>', unsafe_allow_html=True)
        condition_value = None
        rate = None
        item_type = None
        a = None
        b = None
        c = None

    if quantity is None or quantity == 0:
        stock_status = 'Out of Stock'
        status_class = 'out-of-stock'
    elif condition_value is not None and quantity > condition_value:
        stock_status = 'In Stock'
        status_class = 'in-stock'
    elif condition_value is not None:
        stock_status = 'Low Stock'
        status_class = 'low-stock'
    
    # Display results
    st.markdown(f'<p class="result {status_class}">Stock Status: {stock_status}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result">Rate: {rate}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result">Item Type: {item_type}</p>', unsafe_allow_html=True)
    
    # Display matching items if stock status is low or out of stock
    if stock_status == 'Out of Stock' or stock_status == 'Low Stock':
        st.markdown(f'<p class="result">Matching Items: {a}, {b}, {c}</p>', unsafe_allow_html=True)
        
        matching_items = [a, b, c]
        for item in matching_items:
            if item:
                image_path_jpeg = f'{item}.jpeg'  # Adjust the file extension as needed
                if os.path.exists(image_path_jpeg):
                    st.image(image_path_jpeg, caption=f'Image of {item}', use_column_width=True)
                else:
                    st.markdown(f'<p class="result">No image available for {item}</p>', unsafe_allow_html=True)
        
        # Highlighted message for low stock or out of stock
        if stock_status == 'Out of Stock':
            st.markdown('<p class="highlight-red">यह आइटम स्टॉक में नहीं है, कृपया पुष्टि करने के लिए गोदाम में संपर्क करें</p>', unsafe_allow_html=True)
        elif stock_status == 'Low Stock':
            st.markdown('<p class="highlight-yellow">यह आइटम का स्टॉक कम है, कृपया अधिक जानकारी के लिए गोदाम में संपर्क करें</p>', unsafe_allow_html=True)

    # Display image of the selected item
    image_path_jpeg = f'{item_no}.jpeg'  # Adjust the file extension as needed
    if os.path.exists(image_path_jpeg):
        st.image(image_path_jpeg, caption=f'Image of {item_no}', use_column_width=True)
        st.markdown('<p class="highlight-green">यह आइटम स्टॉक में है, कृपया ऑर्डर बुक करने के लिए गोदाम में संपर्क करें</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result">No image available for this ITEM NO.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="result">Please select an ITEM NO.</p>', unsafe_allow_html=True)

# Footer
st.markdown('<p class="footer">Powered by Jyoti Cards</p>', unsafe_allow_html=True)
