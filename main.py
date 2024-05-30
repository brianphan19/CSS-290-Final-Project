import pandas as pd
import matplotlib.pyplot as plt
from scrapper import Scrapper
import threading

# Load the data into a pandas DataFrame
df = pd.read_csv('uspvdb_v1_0_20231108.csv')

# Now you can access the data using the column names you provided
df['p_cap_tot'] = df['p_cap_dc'] + df['p_cap_ac']
df['avg_area'] = df['p_cap_tot'] / df['p_area']

# Function to fetch data using the Scrapper class
def fetch_data(row,  results, index):
    scrapper = Scrapper()
    
    latitude = row['ylat']
    longitude = row['xlong']

    unit_value, unit_label = scrapper.get_unit_value(latitude, longitude)
    scrapper.close()
    results[index] = (row['p_name'], row['p_area'], row['p_cap_ac'], row['p_cap_dc'], unit_value + ' ' + unit_label.replace('arrow_drop_down', ''))

# Select the top 10 rows with the highest z-scores
d = df.nlargest(10, 'p_zscore')
print(d)

# Prepare a list to store the results and threads
results = [None] * len(d)
threads = []
index = 0
# Iterate over the selected rows
for i, row in d.iterrows():
    # Start a new thread for each row
    thread = threading.Thread(target=fetch_data, args=(row, results, index))
    threads.append(thread)
    thread.start()
    index += 1

# Join all threads to ensure they complete
for thread in threads:
    thread.join()

# Print the results
for result in results:
    print(result)