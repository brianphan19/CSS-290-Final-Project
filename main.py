import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
df = pd.read_csv('uspvdb_v1_0_20231108.csv')

# Now you can access the data using the column names you provided
eia_id = df['eia_id']
p_state = df['p_state']
ylat = df['ylat']
xlong = df['xlong']
p_area = df['p_area']
p_name = df['p_name']

p_cap_ac = df['p_cap_ac']
p_cap_dc = df['p_cap_dc']
p_zscore = df['p_zscore']

df['p_cap_tot'] = p_cap_dc + p_cap_ac
df['avg_area'] = df['p_cap_tot'] / df['p_area']



# Example of how to work with the data
print(df.head())  # Prints the first few rows of the dataframe


# plt.figure(figsize=(10, 6))
# plt.scatter(df['avg_area'], df['p_zscore'], color='b')
# plt.title('z score vs efficiency')
# plt.xlabel('Area')
# plt.ylabel('z_score')
# plt.grid(True)
# plt.show()

d = df.nlargest(10, 'p_zscore')
print(d)
