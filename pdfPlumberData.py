import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pdfplumber
import csv
import os
# A function to upload the Mpesa statement PDF and convert it to CSV
def uploadPDF(PDF, csv_path):
    # Open the PDF file
    with pdfplumber.open(PDF) as pdf, open(csv_path, 'w', newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)  # Use the opened file object here
        
        # Iterate through each page
        for page_num, page in enumerate(pdf.pages):
            print(f"Processing page {page_num + 1}")
            
            # Find tables in the page
            tables = page.find_tables(table_settings={
                "vertical_strategy": "text",
                "horizontal_strategy": "lines",
                "intersection_tolerance": 5
            })
            
            for table_num, table in enumerate(tables):
                data = table.extract()
                for row in data:
                    # Replace newline characters with a space
                    row = [cell.replace('\n', ' ') for cell in row]
                    print(row)
                    csv_writer.writerow(row)  # Write each row to the CSV file

    print('Processing completed. The table data has been saved to:', csv_path)
    return csv_path

# Add TransactionIn and TransactionOut columns
def process_transactions(row):
    from_account = 26658687415.0
    if row['From'] != from_account and row['To'] == from_account:
        row['TransactionIn'] = row['Transaction Amount']
        row['TransactionOut'] = 0
    elif row['From'] == from_account and row['To'] != from_account:
        row['TransactionIn'] = 0
        row['TransactionOut'] = row['Transaction Amount']
    else:
        row['TransactionIn'] = 0
        row['TransactionOut'] = 0
    return row

# A function to clean the CSV generated after uploading the csv
def cleanData(csv_path):
    # Specifying the column names
    columnNames = ['Transaction Date', 'From', 'To', 'Transaction Amount', 'Balance', 'Description']

    # Read the CSV file, handling errors and potentially skipping bad lines
    TransactionsCSV = pd.read_csv(csv_path, on_bad_lines='warn', usecols=range(6), names=columnNames)
    TransactionsCSV =  TransactionsCSV.apply(process_transactions, axis=1)

    # Ensure the 'To' column is treated as string
    TransactionsCSV['To'] = TransactionsCSV['To'].fillna('').astype(str).str.replace(',', '')
    # Ensure the 'From' column is treated as string
    TransactionsCSV['From'] = TransactionsCSV['From'].fillna('').astype(str).str.replace('"', '')

    # Clean 'Transaction Date' column by removing extra spaces within the date strings
    TransactionsCSV['Transaction Date'] = TransactionsCSV['Transaction Date'].astype(str).str.replace(" ", "", regex=False)

    # Saving the cleaned data to Transactions_clean.csv
    TransactionsCSV.to_csv("Transactions_functionTestclean.csv", index=False)
    return TransactionsCSV  # Return the DataFrame for further use

# A function to plot the Balance against Transaction Amount
def balanceAgainstTransactionAmount(cleanTransactions):
        # Ensure the necessary columns are numeric for plotting
    cleanTransactions['Transaction Amount'] = pd.to_numeric(cleanTransactions['Transaction Amount'], errors='coerce')
    cleanTransactions['Balance'] = pd.to_numeric(cleanTransactions['Balance'], errors='coerce')

    # Drop rows with missing or non-numeric values in the specified columns
    cleanTransactions = cleanTransactions.dropna(subset=['Transaction Amount','Balance'])

    # Plot Balance against Transaction Amount
    plt.figure(figsize=(10, 6))
    plt.scatter(cleanTransactions['Transaction Amount'], cleanTransactions['Balance'], alpha=0.7, edgecolors='k')
    plt.title('Balance vs. Transaction Amount')
    plt.xlabel('Transaction Amount')
    plt.ylabel('Balance')
    plt.grid(True)
    st.pyplot(plt)

    # a function to Plot TransactionIn and TransactionOut against Transaction Date

# A functionto to plot Transaction In and Out against Transaction Date
def TInAndTOutAgainstTDate(cleanTransactions):
        # Drop rows with missing or invalid 'Transaction Date' after parsing
    cleanTransactions = cleanTransactions.dropna(subset=['Transaction Date'])

    # Ensure 'Transaction Date' is a datetime object
    if not pd.api.types.is_datetime64_any_dtype(cleanTransactions['Transaction Date']):
        cleanTransactions['Transaction Date'] = pd.to_datetime(cleanTransactions['Transaction Date'], errors='coerce')

    # Ensure 'TransactionIn' and 'TransactionOut' are numeric for plotting
    cleanTransactions['TransactionIn'] = pd.to_numeric(cleanTransactions['TransactionIn'], errors='coerce').fillna(0)
    cleanTransactions['TransactionOut'] = pd.to_numeric(cleanTransactions['TransactionOut'], errors='coerce').fillna(0)

    # Plot TransactionIn and TransactionOut against Transaction Date
    plt.figure(figsize=(10, 6))
    plt.plot(cleanTransactions['Transaction Date'], cleanTransactions['TransactionIn'], label='Transaction In', marker='o', linestyle='-', alpha=0.7)
    plt.plot(cleanTransactions['Transaction Date'], cleanTransactions['TransactionOut'], label='Transaction Out', marker='o', linestyle='-', alpha=0.7, color='red')

    # Format the x-axis to display dates properly
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Add labels and title
    plt.title('Transaction In and Out vs. Transaction Date')
    plt.xlabel('Transaction Date')
    plt.ylabel('Transaction Amount')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    st.pyplot(plt)

# A function to plot the Balance against the Transaction Date
def balanceAgainstTime(cleanTransactions):
    # Ensure 'Transaction Date' is a datetime object
    cleanTransactions['Transaction Date'] = pd.to_datetime(cleanTransactions['Transaction Date'], errors='coerce')

# Drop rows with missing or invalid values
    cleanTransactions = cleanTransactions.dropna(subset=['Transaction Date', 'Balance'])
    # Ensure 'Balance' is numeric
    cleanTransactions['Balance'] = pd.to_numeric(cleanTransactions['Balance'], errors='coerce')

    # Debug: Check cleaned data before plotting
    print("Cleaned DataFrame:")
    print(cleanTransactions[['Transaction Date', 'Balance']].head())

    # Plot Balance against Transaction Date
    plt.figure(figsize=(10, 6))
    plt.plot(cleanTransactions['Transaction Date'], cleanTransactions['Balance'], label='Balance', marker='o', linestyle='-', alpha=0.8, color='blue')

     # Format the x-axis to display dates properly
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Add labels, title, and grid
    plt.title('Balance vs. Transaction Date')
    plt.xlabel('Transaction Date')
    plt.ylabel('Balance')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)

    # Display the plot in Streamlit
    st.pyplot(plt.gcf())

# A function to plot Number of Transactions Per Week
    # Sum of TransactionIn Per Week
    # Sum of TransactionOut Per Week
    # Number of Transactions Per Month
    # Sum of TransactionIn Per Month
    # Sum of TransactionOut Per Month
def transactionAnalysis(cleanTransactions):
        # Ensure 'Transaction Date' is a datetime object
    cleanTransactions['Transaction Date'] = pd.to_datetime(cleanTransactions['Transaction Date'], errors='coerce')

    # Drop rows with missing or invalid values in 'Transaction Date'
    cleanTransactions = cleanTransactions.dropna(subset=['Transaction Date'])


    # Ensure numeric columns for TransactionIn and TransactionOut
    cleanTransactions['TransactionIn'] = pd.to_numeric(cleanTransactions['TransactionIn'], errors='coerce')
    cleanTransactions['TransactionOut'] = pd.to_numeric(cleanTransactions['TransactionOut'], errors='coerce')

    # Fill missing values in TransactionIn and TransactionOut
    cleanTransactions['TransactionIn'] = cleanTransactions['TransactionIn'].fillna(0)
    cleanTransactions['TransactionOut'] = cleanTransactions['TransactionOut'].fillna(0)


    # --- Weekly Aggregations ---
    weekly_data = cleanTransactions.groupby(cleanTransactions['Transaction Date'].dt.to_period('W'))
    transactions_per_week = weekly_data.size()  # Count transactions per week
    transaction_in_per_week = weekly_data['TransactionIn'].sum()  # Sum TransactionIn per week
    transaction_out_per_week = weekly_data['TransactionOut'].sum()  # Sum TransactionOut per week

    # --- Monthly Aggregations ---
    monthly_data = cleanTransactions.groupby(cleanTransactions['Transaction Date'].dt.to_period('M'))
    transactions_per_month = monthly_data.size()  # Count transactions per month
    transaction_in_per_month = monthly_data['TransactionIn'].sum()  # Sum TransactionIn per month
    transaction_out_per_month = monthly_data['TransactionOut'].sum()  # Sum TransactionOut per month

    # --- Bar Chart for Transactions Per Week ---
    plt.figure(figsize=(12, 6))
    transactions_per_week.plot(kind='bar', color='lightgreen', alpha=0.8)
    plt.title('Number of Transactions Per Week')
    plt.xlabel('Week')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # --- Bar Chart for TransactionIn Per Week ---
    plt.figure(figsize=(12, 6))
    transaction_in_per_week.plot(kind='bar', color='blue', alpha=0.8)
    plt.title('Sum of TransactionIn Per Week')
    plt.xlabel('Week')
    plt.ylabel('TransactionIn Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # --- Bar Chart for TransactionOut Per Week ---
    plt.figure(figsize=(12, 6))
    transaction_out_per_week.plot(kind='bar', color='red', alpha=0.8)
    plt.title('Sum of TransactionOut Per Week')
    plt.xlabel('Week')
    plt.ylabel('TransactionOut Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # --- Bar Chart for Transactions Per Month ---
    plt.figure(figsize=(12, 6))
    transactions_per_month.plot(kind='bar', color='coral', alpha=0.8)
    plt.title('Number of Transactions Per Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # --- Bar Chart for TransactionIn Per Month ---
    plt.figure(figsize=(12, 6))
    transaction_in_per_month.plot(kind='bar', color='blue', alpha=0.8)
    plt.title('Sum of TransactionIn Per Month')
    plt.xlabel('Month')
    plt.ylabel('TransactionIn Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # --- Bar Chart for TransactionOut Per Month ---
    plt.figure(figsize=(12, 6))
    transaction_out_per_month.plot(kind='bar', color='red', alpha=0.8)
    plt.title('Sum of TransactionOut Per Month')
    plt.xlabel('Month')
    plt.ylabel('TransactionOut Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

#################################################################################################

st.title("M-Pesa statement Analyzer")
st.write("Welcome to the M-Pesa statement Analyzer App")
uploadFile = st.file_uploader("Upload your M-Pesa statement in PDF format", type="pdf")

if uploadFile is not None:
        # Path to the output CSV file
        csv_file_path = 'transactions_functionTest.csv'

        work = uploadPDF(uploadFile, csv_file_path)  # Pass the uploaded file
        cleaned_data = cleanData(work)  # Get cleaned data
        st.write(cleaned_data)  # Display the cleaned DataFrame
        Balance_and_TAmout = balanceAgainstTransactionAmount(cleaned_data) # plot the balance Against Transaction Amount plot
        TransactionIn_and_TransactionOut = TInAndTOutAgainstTDate(cleaned_data)
        balance_Against_Time = balanceAgainstTime(cleaned_data)
        Transaction_Analysis = transactionAnalysis(cleaned_data)
        



# st.title("Hello, Streamlit!")
# st.write("Welcome to your first Streamlit app.")
# st.text_input("Enter your name:")
