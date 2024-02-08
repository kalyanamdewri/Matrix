import pandas as pd

file_path = ''
sheet1 = 'column 1'
sheet2 = 'column_2'
output_file_path = 'new.xlsx'

# Read the sheets into pandas DataFrames
df1 = pd.read_excel(file_path, sheet_name=sheet1, usecols=['Department ID', 'Department'])
df2 = pd.read_excel(file_path, sheet_name=sheet2, usecols=['ID', 'Name'])

# Rename columns for consistency (optional)
df1.rename(columns={'Department ID': 'ID', 'Department': 'Name'}, inplace=True)

# Merge the DataFrames on 'ID' to find matching and unmatching entries
merged_df = pd.merge(df1, df2, on='ID', how='outer', indicator=True)

# Add columns for "Matching/Unmatching" and "Both/SM_Update/SM_Update_2"
merged_df['Matching/Unmatching'] = merged_df['_merge'].replace({'left_only': 'Unmatching', 'right_only': 'Unmatching', 'both': 'Matching'})
merged_df['Both/SM_Update/SM_Update_2'] = merged_df['_merge'].replace({'left_only': 'SM_Update', 'right_only': 'SM_Update_2', 'both': 'Both'})

# Add placeholder columns
merged_df['Email Sent'] = ''
merged_df['Department ID'] = merged_df['ID']
merged_df['Department'] = merged_df['Name_x'].combine_first(merged_df['Name_y'])
merged_df['Verified'] = ''
merged_df['Contact Information'] = ''

# Select and reorder columns as needed
final_columns = ['Matching/Unmatching', 'Both/SM_Update/SM_Update_2', 'Email Sent', 'Department ID', 'Department', 'Verified', 'Contact Information']
final_df = merged_df[final_columns]

# Drop the '_merge' indicator column as it's no longer needed
final_df.drop('_merge', axis=1, inplace=True, errors='ignore')

# Save the DataFrame to a new Excel file
final_df.to_excel(output_file_path, sheet_name='check', index=False)
