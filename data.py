from faker import Faker
import random
import pandas as pd

# Initialize Faker
fake = Faker()

# Your mobile number
your_mobile_number = 55555555

# Generate random transaction data
def generate_transaction_data(num_records=50):
    data = []
    balance = round(random.uniform(0.00, 5000), 2)  # Initial balance
    for _ in range(num_records):
        transaction_date = fake.date_time_this_year()
        from_account = random.choice([your_mobile_number, fake.random_int(min=10000000000, max=99999999999)])
        to_account = random.choice([your_mobile_number, fake.random_int(min=10000000000, max=99999999999)])

        if from_account == your_mobile_number and to_account != your_mobile_number:
            transaction_amount = round(random.uniform(0.01, 1000), 2)
            balance -= transaction_amount
        elif from_account != your_mobile_number and to_account == your_mobile_number:
            transaction_amount = round(random.uniform(0.01, 1000), 2)
            balance += transaction_amount
        else:
            transaction_amount = 0.0
        
        description = random.choice([
            "TwoPartPaybill",
            "Overdraft Payment from {} - Redeem Financial Services".format(from_account),
            "Airtime Purchase",
            "Customer Transfer",
            "Withdrawal Charge",
            "Funds received from {} - {}".format(fake.random_int(min=10000000000, max=99999999999), fake.name()),
            "Customer Withdrawal At Agent Till {}".format(fake.random_int(min=10000, max=99999))
        ])

        data.append({
            "Transaction Date": transaction_date,
            "From": from_account,
            "To": to_account,
            "Transaction Amount": transaction_amount,
            "Balance": round(balance, 2),
            "Description": description
        })
    return data

# Generate data and convert to DataFrame
transactions = generate_transaction_data(100)  # Generate 100 transactions
df = pd.DataFrame(transactions)

# Save to CSV
df.to_csv("transactions2.csv", index=False)

# Print first few rows
print(df.head())
