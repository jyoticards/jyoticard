import streamlit as st
import pandas as pd
import os

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
    }
    .footer {
        font-size: 1em;
        color: #888;
        text-align: center;
        margin-top: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
import pandas as pd

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
    elif condition_value is not None and quantity > condition_value:
        stock_status = 'In Stock'
    elif condition_value is not None:
        stock_status = 'Low Stock'
    
    # Display results
    st.markdown(f'<p class="result">Stock Status: {stock_status}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result">Rate: {rate}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result">Item Type: {item_type}</p>', unsafe_allow_html=True)
    if stock_status == 'Out of Stock' or stock_status == 'Low Stock':
        st.markdown(f'<p class="result">Matching Items: {a}, {b}, {c}</p>', unsafe_allow_html=True)

    # Display image
    image_path = os.path.join('ITEM IMAGES', f'{item_no}.jpeg')  # Adjust the file extension as needed
    if os.path.exists(image_path):
        st.image(image_path, caption=f'Image of {item_no}', use_column_width=True)
    else:
        st.markdown('<p class="result">No image available for this ITEM NO.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="result">Please select an ITEM NO.</p>', unsafe_allow_html=True)

# Footer
st.markdown('<p class="footer">Powered by Jyoti Cards</p>', unsafe_allow_html=True)
