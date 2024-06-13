import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('manufacturing_line_data.csv')

# Basic analysis
total_products = df['Product'].nunique()
average_duration_per_process = df.groupby('Process')['Duration'].mean()
total_time_in_system = df.groupby('Product')['Duration'].sum().mean()
process_counts = df['Process'].value_counts()

print(f'Total products processed: {total_products}')
print(f'Average duration per process:\n{average_duration_per_process}')
print(f'Average total time in the system per product: {total_time_in_system} seconds')
print(f'Process counts:\n{process_counts}')

# Visualization
plt.figure(figsize=(14, 8))

# Histogram of process durations
plt.subplot(2, 2, 1)
df['Duration'].plot(kind='hist', bins=20, alpha=0.75)
plt.title('Distribution of Process Durations')
plt.xlabel('Duration (seconds)')

# Bar plot of average duration per process
plt.subplot(2, 2, 2)
average_duration_per_process.plot(kind='bar', color='skyblue')
plt.title('Average Duration per Process')
plt.ylabel('Duration (seconds)')
plt.xlabel('Process')

# Throughput over time
plt.subplot(2, 1, 2)

# Filter for packaging process to determine completed products
packaging_df = df[df['Process'] == 'Packaging']

# Set the interval for throughput calculation (e.g., every hour, which is 3600 seconds)
interval = 60 * 60  # 1 hour
max_time = df['End'].max()

# Create bins for the time intervals
time_bins = np.arange(0, max_time + interval, interval)

# Count the number of products completed in each time interval
throughput, _ = np.histogram(packaging_df['End'], bins=time_bins)

# Plot the throughput
plt.plot(time_bins[:-1], throughput, marker='o', linestyle='-', color='green')
plt.title('Throughput Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Number of Products Completed')
plt.grid(True)

plt.tight_layout()
plt.show()
