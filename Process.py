import os
import pandas as pd
from datetime import datetime
import numpy as np
import re

def connect_angle_to_frame(folder_path, MR_file, nexus_file_array, nexus_index_file, side, name_of_angle, type_of_angle):
    """
    Link the angle data from the Nexus file with the frame from the MR file to create a unified dataset.
    Parameters:
        folder_path (str): Path to the folder containing the files.
        MR_file (str): Name of the MR file containing the data.
        nexus_file_array (list): List of Nexus files to process.
        nexus_index_file (int): Index of the Nexus file in the list to link.
        side (str): The side for which data is to be extracted (e.g., "Left", "Right").
        name_of_angle (str): Name of the angle to extract.
        type_of_angle (str): Type of angle (X, Y, or Z).
    Returns:
        DataFrame: DataFrame containing the linked frame and angle data.
    """
    df_MR = pd.read_csv(os.path.join(folder_path, MR_file))   
    # Get the corresponding Nexus file from the list
    nexus_file_with_number = nexus_file_array[nexus_index_file]
    df_Nexus = pd.read_csv(os.path.join(folder_path, nexus_file_with_number), skiprows=5)       # skipping the first 5 lines

    # Get the start time from both MR and Nexus files
    MR_time_start = df_MR.iloc[:, 11].iloc[0]  # Get the time from the first row of column 11 in MR file
    Nexus_time_start = df_MR.iloc[:, 11].iloc[nexus_index_file + 2]  # Get the time from the (2+n)-th row of column 11 in MR file

    # Convert time to datetime format
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    MR_time = datetime.strptime(MR_time_start, fmt)
    Nexus_time = datetime.strptime(Nexus_time_start, fmt)

    # Calculate the time difference between MR and Nexus
    time_difference = Nexus_time - MR_time
    time_difference_seconds = time_difference.total_seconds()

    # Calculate the start frame in Nexus based on the time difference
    start_frame_on_nexus = int(time_difference_seconds / 0.01)
    start_frame_on_nexus_to_MR = start_frame_on_nexus + 5

    # Get the starting frame from the previously cut Nexus file
    start_from_cutted_frame = df_Nexus.iloc[0, 0]
    start_frame_on_nexus_to_MR = start_frame_on_nexus_to_MR + int(start_from_cutted_frame)

    # Find the position of "Trajectories" in the Nexus file to remove unnecessary parts
    trajectories_index = df_Nexus.index[df_Nexus.iloc[:, 0] == 'Trajectories'].tolist()

    # If "Trajectories" is found, keep only the rows before it
    if trajectories_index:
        df_Nexus = df_Nexus.iloc[:trajectories_index[0]]

    # Get frames from MR file starting from the determined frame
    frames_MR = df_MR.iloc[start_frame_on_nexus_to_MR:, 0].reset_index(drop=True)

    def get_index_of_column(path, side, name_of_angle, type_of_angle):
        def read_csv_with_skiprows(path):
            # Read CSV file and determine how many rows to skip based on the filename
            filename = os.path.basename(path)
            skiprows = 3 if re.search(r'\d', filename) else 3
            df = pd.read_csv(path, skiprows=skiprows)
            return df
        
        df = read_csv_with_skiprows(path)
        pattern = f".*{side}{name_of_angle}$"  # Create pattern to find the column name containing the angle
        # Return the column index based on angle type (X, Y, or Z)
        if type_of_angle == 'X':
            return next((i for i, col in enumerate(df.columns) if re.match(pattern, col)), None)
        if type_of_angle == 'Y':
            return next((i for i, col in enumerate(df.columns) if re.match(pattern, col)), None) + 1
        if type_of_angle == 'Z':
            return next((i for i, col in enumerate(df.columns) if re.match(pattern, col)), None) + 2

    # Find the column index containing the angle to plot in the Nexus file
    index_of_column = get_index_of_column(os.path.join(folder_path, nexus_file_with_number), side, name_of_angle, type_of_angle)
    # Get angle data from the corresponding column in Nexus
    columns_from_nexus = df_Nexus.iloc[0:, [0, index_of_column]].reset_index(drop=True)
    # Get the length of Nexus data to trim the DataFrame
    length_of_nexus = len(columns_from_nexus)
    # Combine frame data from MR and angle data from Nexus
    conect_frame_angle = pd.concat([frames_MR[:length_of_nexus], columns_from_nexus[:length_of_nexus]], axis=1)

    # Set column names for the resulting DataFrame
    conect_frame_angle.columns = ['frame', 'index_on_nexus', 'angle']
    conect_frame_angle = conect_frame_angle.dropna(subset=['frame'])
    conect_frame_angle['frame'] = ((conect_frame_angle['frame'].astype(float)) * 100).astype(int)

    return conect_frame_angle


def create_combined_dataframe(folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle):
    combined_dataframe = pd.DataFrame()   
    # Loop through each index in nexus_file_array
    for nexus_index_file in range(len(nexus_file_array)):
        # Link angle with frame and create DataFrame
        df = connect_angle_to_frame(folder_path, MR_file, nexus_file_array, nexus_index_file, side, name_of_angle, type_of_angle)
        # Concatenate DataFrame vertically
        combined_dataframe = pd.concat([combined_dataframe, df], ignore_index=True)
    return combined_dataframe

def create_table_of_angle(processed_file_path, folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle,drop_row_in_processed_file=None):
    df_processed = pd.read_csv(processed_file_path)
    # Remove unnecessary rows if the algorithm couldn't process them
    if drop_row_in_processed_file is not None:
        df_processed = df_processed.drop(drop_row_in_processed_file).reset_index(drop=True)

 
    # Create a new DataFrame from the create_combined_dataframe function
    new_dataframe = create_combined_dataframe(folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle)
    
    # Assume that the second column of df_processed contains the start frame and the third column contains the end frame
    start_frames = df_processed.iloc[:, 1]
    end_frames = df_processed.iloc[:, 2]
    angles_in_cycles = []
    # Get the first and last frame values from new_dataframe
    first_frame = new_dataframe['frame'].iloc[0]
    last_frame = new_dataframe['frame'].iloc[-1]

    # Loop through each start and end frame pair
    for start_frame, end_frame in zip(start_frames, end_frames):
        # Check if the start frame is greater than or equal to the first frame in new_dataframe
        if start_frame >= first_frame:
            cycle_angles = []   
            cycle_frames = []   
            # Loop through the frames in new_dataframe to find frames within the cycle range
            for frame in new_dataframe['frame']:
                # If the frame is within the cycle from start_frame to end_frame
                if frame >= start_frame:
                    if frame <= end_frame:
                        cycle_angles.append(new_dataframe.loc[new_dataframe['frame'] == frame, 'angle'].values[0])
                        cycle_frames.append(frame)
                    else:
                        break  # Stop when frame exceeds end_frame

            # Check if the cycle contains frames from start_frame to end_frame
            if len(cycle_frames) > 0 and cycle_frames[0] == start_frame and cycle_frames[-1] == end_frame:
                angles_in_cycles.append(cycle_angles)  # Add cycle to the angles_in_cycles list

            # Stop if end_frame exceeds the last frame in new_dataframe
            if end_frame > last_frame:
                break

    # Return a DataFrame where each column represents a cycle, and the rows contain angles for each frame in that cycle
    return pd.DataFrame(angles_in_cycles).T


def create_combined_angle_table(folder_path, processed_file_path, MR_file, nexus_file_array, sides, name_of_angles, types_of_angles,drop_row_in_processed_file):
    combined_df = pd.DataFrame()   
    # Loop through each side, angle name, and angle type
    for side, name_of_angle, type_of_angle in zip(sides, name_of_angles, types_of_angles):
        # Create the angle table for each side, angle name, and angle type
        df_angle = create_table_of_angle(processed_file_path, folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle,drop_row_in_processed_file)
        
        # Set column names in the DataFrame based on side, angle name, and angle type
        df_angle.columns = [f"{side}_{name_of_angle}_{type_of_angle}_cycle_{i+1}" for i in range(df_angle.shape[1])]
 
        combined_df = pd.concat([combined_df, df_angle], axis=1)
    return combined_df


def calculate_phase_means(df):
    avg_stance = df.iloc[:, 4].mean()
    avg_initial_swing = df.iloc[:, 6].mean() + avg_stance
    avg_mid_swing = df.iloc[:, 8].mean() + avg_initial_swing
    return avg_stance, avg_initial_swing, avg_mid_swing

 
def calculate_mean_and_std_angles(result_df):
    # Define percentages from 0% to 100%
    percentages = np.linspace(0, 100, 101)  # 101 points from 0 to 100%
    mean_angles_at_percentages = []
    std_angles_at_percentages = []

    # Loop through each percentage point
    for x in percentages:
        angles_at_x = []

        # Iterate over each column (representing a gait cycle)
        for i in range(len(result_df.columns)):
            angles_column = result_df.iloc[:, i]  # Get the current column (cycle)

            # Calculate the cycle length excluding NaN values
            T = len(angles_column.dropna())

            # Find the frame index at the current percentage of the cycle
            frame_index_at_x = int(T * (x / 100))  # Calculate the frame index at x%

            if frame_index_at_x < T:
                # Retrieve the angle at the calculated frame index
                angle_at_x = pd.to_numeric(angles_column.iloc[frame_index_at_x], errors='coerce')
                if not np.isnan(angle_at_x):  # Skip NaN values
                    angles_at_x.append(angle_at_x)

        # Calculate the mean and standard deviation angle for this percentage point
        if angles_at_x:
            mean_angle_at_x = np.mean(angles_at_x)
            std_angle_at_x = np.std(angles_at_x)
            mean_angles_at_percentages.append(mean_angle_at_x)
            std_angles_at_percentages.append(std_angle_at_x)

    return mean_angles_at_percentages, std_angles_at_percentages
 