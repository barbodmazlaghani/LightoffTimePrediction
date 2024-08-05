import pandas as pd
import os

from matplotlib import pyplot as plt


def load_csv_files(folder_path):
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    return csv_files



def process_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    csv_files = load_csv_files(input_folder)

    fuel_cunsomption = []
    i =0
    for file_path in csv_files:
        df = pd.read_csv(file_path)
        fuel_cunsomption.append((df["Trip_fuel_consumption"].max() - df["Trip_fuel_consumption"].min()) / (df["Cumulative_mileage"].max() - df["Cumulative_mileage"].min()) / 10000)
        i=i+1
    # Combine all vehicle speeds into a single DataFrame for plotting
    # combined_speeds = pd.concat(vehicle_speeds, ignore_index=True)

    # Plot the box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(fuel_cunsomption)
    plt.title('Box Plot of Fuel Consumption - Augmented Data')
    plt.ylabel('Fuel Consumption (L per 100 Km)')
    plt.savefig(os.path.join(output_folder, 'fuel_consumption_box_plot.Augmented.png'))
    plt.show()
    print (i)


# Paths to the folders
input_folder = '04_Augmented Corrected Slices (second algo.)'
output_folder = 'corrected_slices'

# Process the files
process_files(input_folder, output_folder)