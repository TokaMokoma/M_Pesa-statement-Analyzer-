import pandas as pd
import tabula

# area = [100,50,200,400]
# columns =[60,150,250,350]


dfs = tabula.read_pdf('DOC-20250101-WA0023..pdf',guess=True,stream=True, pages='all')

# df.to_csv('mpesaStatement.csv',index=False)

# Assuming you want to save all tables into one CSV
# Concatenate all DataFrames in the list into a single DataFrame
df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to a CSV file
df.to_csv('mpesaStatement.csv', index=False)