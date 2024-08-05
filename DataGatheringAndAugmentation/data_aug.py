import os
import pandas as pd
import itertools
import seaborn as sns

def load_csv_files(folder_path, num_slices):
    slices = []
    for i in range(1, num_slices + 1):
        file_path = os.path.join(folder_path, f'slice_{i}.csv')
        if os.path.exists(file_path):
            temp_df = pd.read_csv(file_path)
            temp_df['slice'] = os.path.basename(file_path)  # Add slice column with the file name
            slices.append(temp_df)
        else:
            print(f'File {file_path} does not exist.')
    return slices

def divide_into_sections_by_temperature(df):
    min_temp = df['Coolant_temperature'].min()
    max_temp = df['Coolant_temperature'].max()
    temp_range = max_temp - min_temp
    first_threshold = min_temp + temp_range / 3
    second_threshold = min_temp + 2 * temp_range / 3

    section1 = df[df['Coolant_temperature'] <= first_threshold]
    section2 = df[(df['Coolant_temperature'] > first_threshold) & (df['Coolant_temperature'] <= second_threshold)]
    section3 = df[df['Coolant_temperature'] > second_threshold]

    return [section1, section2, section3]


def find_matching_sections(sections, target_value, tolerance=1):
    matching_sections = []
    for section in sections:
        if len(section) > 0 and abs(section['Coolant_temperature'].iloc[0] - target_value) <= tolerance:
            matching_sections.append(section)
    return matching_sections


def save_combined_csv(sections, output_folder, base_name):
    os.makedirs(output_folder, exist_ok=True)

    for i in range(1, len(sections)):
        for column in ['time', 'Trip_fuel_consumption', 'Cumulative_mileage']:
            adjustment_value = sections[i-1][column].iloc[-1] - sections[i][column].iloc[0]
            sections[i][column] += adjustment_value

    combined_df = pd.concat(sections).reset_index(drop=True)
    combined_df.to_csv(os.path.join(output_folder, f'{base_name}.csv'), index=False)


# Paths to the folders
folder_path_1 = '02_Corrected Data/slices_1_time_corrected'
folder_path_2 = '02_Corrected Data/slices_2_time_corrected'

# Load the slices
slices_1 = load_csv_files(folder_path_1, 17)
slices_2 = load_csv_files(folder_path_2, 8)

all_slices = slices_1 + slices_2

output_folder = 'augmented_slices_v2'

# Divide each slice into three sections
first_sections = []
second_sections = []
third_sections = []

for slice_df in all_slices:
    sections = divide_into_sections_by_temperature(slice_df)
    if len(sections) == 3:
        first_sections.append(sections[0])
        second_sections.append(sections[1])
        third_sections.append(sections[2])

# Generate augmented slices
combination_count = 1
for i, first_section in enumerate(first_sections):
    matching_second_sections = find_matching_sections(second_sections, first_section['Coolant_temperature'].iloc[-1])
    if not matching_second_sections:
        continue

    for second_section in matching_second_sections:
        matching_third_sections = find_matching_sections(third_sections, second_section['Coolant_temperature'].iloc[-1])
        if not matching_third_sections:
            continue

        for third_section in matching_third_sections:
            augmented_sections = [first_section, second_section, third_section]
            save_combined_csv(augmented_sections, output_folder, f'augmented_slice_{combination_count}')
            combination_count += 1

print("Data augmentation completed.")

# import os
# import pandas as pd
# import matplotlib.pyplot as plt
#
#
# def make_time_increasing(df):
#     # Ensure the time column is sorted by index
#     df = df.sort_index()
#
#     # Create a new column for the adjusted time values
#     df['adjusted_time'] = df['time']
#
#     # Initialize the previous maximum value
#     previous_max = df['time'].iloc[0]
#
#     # Iterate through the time column and replace downward spikes
#     for i in range(1, len(df)):
#         current_value = df['time'].iloc[i]
#         if current_value < previous_max:
#             df['adjusted_time'].iloc[i] = previous_max
#         else:
#             previous_max = current_value
#
#     df['time'] = df['adjusted_time']
#
#     # Drop the temporary adjusted_time column
#     df = df.drop(columns=['adjusted_time'])
#
#     return df
# # def correct_time_spikes(df):
# #     time_values = df['time'].values
# #     corrected_time_values = [time_values[0]]
# #
# #     for i in range(1, len(time_values)):
# #         if time_values[i] < corrected_time_values[-1]:
# #             # Calculate the difference and interpolate
# #             drop_diff = corrected_time_values[-1] - time_values[i]
# #             corrected_time_values.append(corrected_time_values[-1] + drop_diff / (len(time_values) - i))
# #             for j in range(i + 1, len(time_values)):
# #                 corrected_time_values.append(corrected_time_values[-1] + (time_values[j] - time_values[j - 1]))
# #             break
# #         else:
# #             corrected_time_values.append(time_values[i])
# #
# #     df['time'] = corrected_time_values
# #     return df
#
#
# def load_csv_files(folder_path, num_slices):
#     slices = []
#     for i in range(1, num_slices + 1):
#         file_path = os.path.join(folder_path, f'slice_{i}.csv')
#         if os.path.exists(file_path):
#             temp_df = pd.read_csv(file_path)
#             slices.append(temp_df)
#         else:
#             print(f'File {file_path} does not exist.')
#     return slices

# #
# # def divide_into_sections_by_temperature(df):
# #     min_temp = df['Coolant_temperature'].min()
# #     max_temp = df['Coolant_temperature'].max()
# #     temp_range = max_temp - min_temp
# #     first_threshold = min_temp + temp_range / 3
# #     second_threshold = min_temp + 2 * temp_range / 3
# #
# #     section1 = df[df['Coolant_temperature'] <= first_threshold]
# #     section2 = df[(df['Coolant_temperature'] > first_threshold) & (df['Coolant_temperature'] <= second_threshold)]
# #     section3 = df[df['Coolant_temperature'] > second_threshold]
# #
# #     return [section1, section2, section3]
# #
# #
# # def find_matching_sections(sections, target_value, tolerance=1):
# #     matching_sections = []
# #     for section in sections:
# #         if len(section) > 0 and abs(section['Coolant_temperature'].iloc[0] - target_value) <= tolerance:
# #             matching_sections.append(section)
# #     return matching_sections
# #
# #
# # def save_combined_csv(sections, output_folder, base_name):
# #     os.makedirs(output_folder, exist_ok=True)
# #     combined_df = pd.concat(sections).reset_index(drop=True)
# #     combined_df.to_csv(os.path.join(output_folder, f'{base_name}.csv'), index=False)
#
#
# # Paths to the folders
# folder_path_1 = 'slices_1_time_corrected'
# folder_path_2 = 'slices_2_time_corrected'
#
# # Load the slices
# slices_1 = load_csv_files(folder_path_1, 17)
# slices_2 = load_csv_files(folder_path_2, 12)
#
# # Combine all slices
# all_slices = slices_1 + slices_2
#
# # Correct time spikes in all slices
# # all_slices = [make_time_increasing(df) for df in all_slices]
#
# # Plotting
# colors = plt.cm.get_cmap('tab20', len(all_slices))  # Get a colormap with enough colors
#
# plt.figure(figsize=(12, 8))
#
# # Plot each slice with a different color
# for i, df in enumerate(all_slices):
#     plt.plot(df['time'], df['Coolant_temperature'], label=f'Slice {i + 1}', color=colors(i))
#
# plt.xlabel('Time')
# plt.ylabel('Coolant Temperature')
# plt.title('Coolant Temperature vs Time for All Slices')
# plt.legend(loc='best', bbox_to_anchor=(1.05, 1), fontsize='small')
# plt.tight_layout()
# plt.show()
#
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
#
# def load_csv_files(folder_path, num_slices):
#     slices = []
#     for i in range(1, num_slices + 1):
#         file_path = os.path.join(folder_path, f'slice_{i}.csv')
#         if os.path.exists(file_path):
#             temp_df = pd.read_csv(file_path)
#             slices.append(temp_df)
#         else:
#             print(f'File {file_path} does not exist.')
#     return slices
#
# def adjust_mileage_to_start_from_zero(df, mileage_column='Cumulative_mileage'):
#     initial_mileage = df[mileage_column].iloc[0]
#     df[mileage_column] = df[mileage_column] - initial_mileage
#     return df
#
# folder_path_1 = 'slices_1_time_corrected'
# folder_path_2 = 'slices_2_time_corrected'
#
# # Load the slices
# slices_1 = load_csv_files(folder_path_1, 17)
# slices_2 = load_csv_files(folder_path_2, 12)
#
# # Combine all slices
# all_slices = slices_1 + slices_2
#
# # Adjust mileage for each slice to start from zero
# all_slices = [adjust_mileage_to_start_from_zero(df) for df in all_slices]

# # Plotting
# colors = plt.cm.get_cmap('tab20', len(all_slices))  # Get a colormap with enough colors
#
# plt.figure(figsize=(12, 8))
#
# # Plot each slice with a different color
# for i, df in enumerate(all_slices):
#     plt.plot(df['Cumulative_mileage'], df['Coolant_temperature'], label=f'Slice {i + 1}', color=colors(i))
#
# plt.xlabel('Cumulative Mileage (Starting from Zero)')
# plt.ylabel('Coolant Temperature')
# plt.title('Coolant Temperature vs Cumulative Mileage for All Slices')
# plt.legend(loc='best', bbox_to_anchor=(1.05, 1), fontsize='small')
# plt.tight_layout()
# plt.show()
# time_values = []
# cumulative_mileage_values = []
#
# for slice_df in all_slices:
#     if len(slice_df) >= 50:
#         target_row = slice_df.iloc[-50]
#         time_values.append(target_row['time'])
#         cumulative_mileage_values.append(target_row['Cumulative_mileage'])
#
# # Create a DataFrame for plotting
# data = pd.DataFrame({
#     'time': time_values,
#     'Cumulative_mileage': cumulative_mileage_values
# })
#
# # Create box plots for 'time' and 'Cumulative_mileage'
# plt.figure(figsize=(12, 6))
#
# # Box plot for 'time'
# plt.subplot(1, 2, 1)
# sns.boxplot(y=data['time'])
# plt.title('Box Plot for Time (Row[last-50] from all slices)')
#
# # Box plot for 'Cumulative_mileage'
# plt.subplot(1, 2, 2)
# sns.boxplot(y=data['Cumulative_mileage'])
# plt.title('Box Plot for Cumulative Mileage (Row[last-50] from all slices)')
#
# plt.tight_layout()
# plt.show()

