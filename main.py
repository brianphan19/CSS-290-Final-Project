import pandas as pd
import matplotlib.pyplot as plt
from scrapper import Scrapper
import threading
import re
import numpy as np
import matplotlib.cm as cm

# Load the data into a pandas DataFrame
df = pd.read_csv('uspvdb_v1_0_20231108.csv')

# Now you can access the data using the column names you provided
df['p_cap_tot'] = df['p_cap_dc'] + df['p_cap_ac']
df['avg_area'] = df['p_cap_tot'] / df['p_area']

# Function to fetch data using the Scrapper class
def fetch_data(row, results, index, semaphore):
    semaphore.acquire()  # Acquire semaphore to limit the number of threads
    try:
        scrapper = Scrapper()
        
        latitude = row['ylat']
        longitude = row['xlong']

        unit_value = scrapper.get_unit_value(latitude, longitude)
        scrapper.close()
        numeric_value = int(float(re.findall(r"[-+]?\d*\.\d+|\d+", unit_value)[0]))
        results[index] = (row['p_name'], row['p_area'], row['p_cap_ac'], row['p_cap_dc'], numeric_value)
    finally:
        semaphore.release()  # Release semaphore after scraping is done

# Select the top 100 rows with the highest z-scores
d = df.nlargest(500, 'p_zscore')

# Prepare a list to store the results and threads
results = [None] * len(d)
threads = []
index = 0

# Create a semaphore with a maximum of 10 permits (allowing 10 tabs to be opened at a time)
max_threads = 20
semaphore = threading.Semaphore(max_threads)

# Iterate over the selected rows
for i, row in d.iterrows():
    # Start a new thread for each row
    thread = threading.Thread(target=fetch_data, args=(row, results, index, semaphore))
    threads.append(thread)
    thread.start()
    index += 1

# Join all threads to ensure they complete
for thread in threads:
    thread.join()

# Print the results
for result in results:
    print(result)

filtered_results = [result for result in results if result[4] is not None]

# Convert results to a DataFrame for plotting
results_df = pd.DataFrame(filtered_results, columns=['p_name', 'p_area', 'p_cap_ac', 'p_cap_dc', 'unit_value'])

# Create a unique color for each name
unique_names = results_df['p_name'].unique()
colors = cm.rainbow(np.linspace(0, 1, len(unique_names)))
color_map = dict(zip(unique_names, colors))

# Create the scatter plot
plt.figure(figsize=(10, 6))

for name, color in color_map.items():
    subset = results_df[results_df['p_name'] == name]
    plt.scatter(subset['p_area'], subset['unit_value'], label=name, color=color, alpha=0.7)

plt.title('Area vs Unit Value')
plt.xlabel('Area (m^2)')
plt.ylabel('Unit Value (kWh/kWp)')
plt.grid(True)
plt.show()
