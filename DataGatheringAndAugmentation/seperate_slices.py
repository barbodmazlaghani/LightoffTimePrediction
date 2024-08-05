import pandas as pd


file_path = 'Device_QTVq_Data_06_20_2024, 15_24_00_to_07_07_2024, 15_24_00.xlsx'
xls = pd.ExcelFile(file_path)

df_data = pd.read_excel(xls, 'Data')

slices = []
coolant_temp_col = 'Coolant_temperature'
slice_start = None
previous_value = None

for i in range(len(df_data)):
    current_value = df_data.loc[i, coolant_temp_col]

    if slice_start is None and current_value < 40:
        slice_start = i
    elif slice_start is not None:
        if previous_value is not None and previous_value - current_value >= 5:
            if current_value >= 40:
                slice_start = None
            else:
                slice_start = i

        elif current_value >= 85:
            slice_end = i + 50
            slices.append(df_data.iloc[slice_start:slice_end])
            slice_start = None

    previous_value = current_value

for i, slice_df in enumerate(slices):
    output_path = f'slices_1/slice_{i + 1}.csv'
    slice_df.to_csv(output_path, index=False)

slice_files = [f'slice_{i + 1}.csv' for i in range(len(slices))]
print(slice_files)
