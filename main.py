import pandas as pd
import matplotlib.pyplot as plt
from scrapper import Scrapper
import threading
import re
import numpy as np
import matplotlib.cm as cm

# Load the data into a pandas DataFrame
df = pd.read_csv('uspvdb_v1_0_20231108.csv')

# Select the top 10 rows with the highest z-scores
top_farms = df.nlargest(10, 'p_zscore')
print(top_farms)

# Function to fetch data using the Scrapper class
def fetch_data(row,  results, index):
    scrapper = Scrapper()
    
    latitude = row['ylat']
    longitude = row['xlong']

    unit_value = scrapper.get_unit_value(latitude, longitude)
    scrapper.close()
    numeric_value = int(float(re.findall(r"[-+]?\d*\.\d+|\d+", unit_value)[0]))
    results[index] = (row['p_name'], row['p_area'], row['p_cap_ac'], row['p_cap_dc'], numeric_value)

# Prepare a list to store the results and threads
results = [None] * len(top_farms)
threads = []
index = 0
# Iterate over the selected rows
for i, row in top_farms.iterrows():
    # Start a new thread for each row
    thread = threading.Thread(target=fetch_data, args=(row, results, index))
    threads.append(thread)
    thread.start()
    index += 1

# Join all threads to ensure they complete
for thread in threads:
    thread.join()

# Convert results to a DataFrame for plotting
results_df = pd.DataFrame(results, columns=['p_name', 'p_area', 'p_cap_ac', 'p_cap_dc', 'unit_value'])

# Create a unique color for each name
# unique_names = results_df['p_name'].unique()
# colors = cm.rainbow(np.linspace(0, 1, len(unique_names)))
# color_map = dict(zip(unique_names, colors))

# # Create the scatter plot
# plt.figure(figsize=(10, 6))

# for name, color in color_map.items():
#     subset = results_df[results_df['p_name'] == name]
#     plt.scatter(subset['p_area'], subset['unit_value'], label=name, color=color, alpha=0.7)

plt.figure(figsize=(12, 8))
plt.bar(results_df['p_name'], results_df['unit_value'], color='skyblue')
plt.xlabel('Plant Names')
plt.ylabel('Solar ouput (kWh/kWp)')
plt.title('Current solar output of Top 10 Farms')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

