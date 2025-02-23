# from Process import create_table_of_angle,calculate_mean_and_std_angles,calculate_phase_means
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# import pandas as pd
# from scipy.ndimage import uniform_filter1d

# def plot_all_cycle(processed_file_path, folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle,drop_row_in_processed_file):
#     output_folder_path = os.path.join(folder_path, 'Chart2')
#     os.makedirs(output_folder_path, exist_ok=True)

#     table_of_angle = create_table_of_angle(processed_file_path, folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle,drop_row_in_processed_file)

#     # Convert all columns to numeric and drop NaNs
#     for i in range(table_of_angle.shape[1]):
#         table_of_angle.iloc[:, i] = pd.to_numeric(table_of_angle.iloc[:, i], errors='coerce')

#     plt.figure(figsize=(12, 8))

#     # Plot each column with smoothing
#     for i in range(table_of_angle.shape[1]):
#         data = table_of_angle.iloc[:, i].dropna().astype(float)  # Convert to float
        
#         # Apply smoothing to the data
#         if len(data) > 0:  # Ensure there is data to plot
#             smoothed_data = uniform_filter1d(data, size=2)  # Adjust size for smoothing level
#             plt.plot(smoothed_data, label=f'Column {i+1}', linewidth=2)  # No marker

#     plt.title(f"{name_of_angle}_{type_of_angle}_{side}")
#     plt.xlabel('Index')
#     plt.ylabel('Values')
#     plt.grid(True)
#     plot_path = os.path.join(output_folder_path, f"{name_of_angle}_{type_of_angle}_{side}.png")
#     plt.savefig(plot_path, format="png")
#     plt.close() 



# def plot_mean_angles_with_phases(folder_path, name_of_angle, type_of_angle, table_of_angle_left, mean_phase_left, mean_phase_right):
#     # Calculate mean and standard deviation angles across percentages for both legs
#     left_mean_angles, left_std_angles = calculate_mean_and_std_angles(table_of_angle_left)
  
#     percentages = np.linspace(0, 100, 100)

#     # Apply a smoothing filter (moving average)
#     left_mean_angles_smooth = uniform_filter1d(left_mean_angles, size=2)
 
#     left_std_angles_smooth = uniform_filter1d(left_std_angles, size=2)
  
#     # Calculate phase means for both legs
#     left_avg_stance, left_avg_initial_swing, left_avg_mid_swing = calculate_phase_means(mean_phase_left)
#     right_avg_stance, right_avg_initial_swing, right_avg_mid_swing = calculate_phase_means(mean_phase_right)

#     # Define x values for vertical lines and labels for both legs
#     left_x_values = [left_avg_stance * 100, left_avg_initial_swing * 100, left_avg_mid_swing * 100]
#     right_x_values = [right_avg_stance * 100, right_avg_initial_swing * 100, right_avg_mid_swing * 100]
#     label_positions = [0, left_avg_stance * 100, left_avg_initial_swing * 100, left_avg_mid_swing * 100]
#     labels = ['Stance phase', 'Initial swing', 'Mid swing', 'Terminal swing']

#     plt.figure(figsize=(12, 8))
    
#     # Plot smoothed mean angles for left leg
#     plt.plot(percentages, left_mean_angles_smooth, label="Average left", color='red', linewidth=2)
#     plt.fill_between(percentages, 
#                      left_mean_angles_smooth - left_std_angles_smooth, 
#                      left_mean_angles_smooth + left_std_angles_smooth, 
#                      color='red', alpha=0.2)
#     # Plot smoothed mean angles for right leg
 

#     # Plot phase lines and labels
#     for x in left_x_values:
#         plt.axvline(x=x, color='red', linestyle='--', linewidth=1.5)
#     for x in right_x_values:
#         plt.axvline(x=x, color='blue', linestyle='--', linewidth=1.5)

#     # Get the lowest y-axis value for placing labels
#     y_min = plt.gca().get_ylim()[0]
#     # Plot labels at the desired positions
#     for pos, label in zip(label_positions, labels):
#         plt.text(pos + 0.5, y_min - 0.05 * abs(y_min), label, rotation=90, verticalalignment='bottom', color='red', fontsize=12)
#     plt.xlim(-10, 110)
#     plt.xlabel('Normalized (percent)', fontsize=15)
#     plt.ylabel('Angle (degree)', fontsize=15)
#     plt.title(f"{name_of_angle}_{type_of_angle}", fontsize=20)
#     plt.xticks(range(0, 101, 10), fontsize=10)
#     plt.tick_params(axis='x', which='both', length=5, direction='inout')
#     plt.minorticks_on()
#     plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))
#     plt.tick_params(axis='x', which='minor', length=3, direction='inout')
#     plt.grid(True)
#     plt.legend()
#     output_folder_path = os.path.join(folder_path, 'Chart2')
#     os.makedirs(output_folder_path, exist_ok=True)
#     plot_path = os.path.join(output_folder_path, f"{name_of_angle}_{type_of_angle}.png")
#     plt.savefig(plot_path, format="png")
#     plt.close()


# # def save_all(processed_file_path_left,processed_file_path_right,folder_path,MR_file,nexus_file_array,drop_row_in_processed_file):
# #     name_of_angle = ['AnkleAngles','HipAngles','PelvisAngles','KneeAngles']
# #     type_of_angle = ['X','Y','Z']
    
# #     mean_phase_left = pd.read_csv(processed_file_path_left)
# #     mean_phase_right = pd.read_csv(processed_file_path_right)
 
# #     for i in name_of_angle:
# #         for j in type_of_angle:
# #             #plot mean + std on same chart
# #             table_of_angle_left = create_table_of_angle(processed_file_path_left,folder_path, MR_file, nexus_file_array,side= 'L' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
# #             table_of_angle_right = create_table_of_angle(processed_file_path_right,folder_path, MR_file, nexus_file_array,side= 'R' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
# #             plot_mean_angles_with_phases(folder_path,name_of_angle = i,type_of_angle = j,table_of_angle_left = table_of_angle_left, table_of_angle_right=table_of_angle_right, mean_phase_left=mean_phase_left, mean_phase_right=mean_phase_right)
# #             #plot all cycle lines
# #             plot_all_cycle(processed_file_path_left, folder_path, MR_file, nexus_file_array,side= 'L' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
# #             plot_all_cycle(processed_file_path_right, folder_path, MR_file, nexus_file_array,side= 'R' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)


# def save_all(processed_file_path_left,processed_file_path_right,folder_path,MR_file,nexus_file_array,drop_row_in_processed_file):
#     name_of_angle = ['CPD angle','Frontal pelvic tilt','Left Foot angle','Right Foot angle']
#     type_of_angle = ['Z']
    
#     mean_phase_left = pd.read_csv(processed_file_path_left)
#     mean_phase_right = pd.read_csv(processed_file_path_right)
 
#     for i in name_of_angle:
#         for j in type_of_angle:
#             #plot mean + std on same chart
#             table_of_angle_left = create_table_of_angle(processed_file_path_left,folder_path, MR_file, nexus_file_array,side= 'L' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
            
#             plot_mean_angles_with_phases(folder_path,name_of_angle = i,type_of_angle = j,table_of_angle_left = table_of_angle_left, mean_phase_left=mean_phase_left, mean_phase_right=mean_phase_right)
#             #plot all cycle lines
#             plot_all_cycle(processed_file_path_left, folder_path, MR_file, nexus_file_array,side= 'L' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
  
from Process import create_table_of_angle,calculate_mean_and_std_angles,calculate_phase_means
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import uniform_filter1d

def plot_all_cycle(processed_file_path, folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle,drop_row_in_processed_file):
    output_folder_path = os.path.join(folder_path, 'Chart')
    os.makedirs(output_folder_path, exist_ok=True)

    table_of_angle = create_table_of_angle(processed_file_path, folder_path, MR_file, nexus_file_array, side, name_of_angle, type_of_angle,drop_row_in_processed_file)

    # Convert all columns to numeric and drop NaNs
    for i in range(table_of_angle.shape[1]):
        table_of_angle.iloc[:, i] = pd.to_numeric(table_of_angle.iloc[:, i], errors='coerce')

    plt.figure(figsize=(12, 8))

    # Plot each column with smoothing
    for i in range(table_of_angle.shape[1]):
        data = table_of_angle.iloc[:, i].dropna().astype(float)  # Convert to float
        
        # Apply smoothing to the data
        if len(data) > 0:  # Ensure there is data to plot
            smoothed_data = uniform_filter1d(data, size=2)  # Adjust size for smoothing level
            plt.plot(smoothed_data, label=f'Column {i+1}', linewidth=2)  # No marker

    plt.title(f"{name_of_angle}_{type_of_angle}_{side}")
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.grid(True)
    plot_path = os.path.join(output_folder_path, f"{name_of_angle}_{type_of_angle}_{side}.png")
    plt.savefig(plot_path, format="png")
    plt.close() 



def plot_mean_angles_with_phases(folder_path, name_of_angle, type_of_angle, table_of_angle_left, table_of_angle_right, mean_phase_left, mean_phase_right):
    # Calculate mean and standard deviation angles across percentages for both legs
    left_mean_angles, left_std_angles = calculate_mean_and_std_angles(table_of_angle_left)
    right_mean_angles, right_std_angles = calculate_mean_and_std_angles(table_of_angle_right)
    percentages = np.linspace(0, 100, 100)

    # Apply a smoothing filter (moving average)
    left_mean_angles_smooth = uniform_filter1d(left_mean_angles, size=2)
    right_mean_angles_smooth = uniform_filter1d(right_mean_angles, size=2)
    left_std_angles_smooth = uniform_filter1d(left_std_angles, size=2)
    right_std_angles_smooth = uniform_filter1d(right_std_angles, size=2)

    # Calculate phase means for both legs
    left_avg_stance, left_avg_initial_swing, left_avg_mid_swing = calculate_phase_means(mean_phase_left)
    right_avg_stance, right_avg_initial_swing, right_avg_mid_swing = calculate_phase_means(mean_phase_right)

    # Define x values for vertical lines and labels for both legs
    left_x_values = [left_avg_stance * 100, left_avg_initial_swing * 100, left_avg_mid_swing * 100]
    right_x_values = [right_avg_stance * 100, right_avg_initial_swing * 100, right_avg_mid_swing * 100]
    label_positions = [0, left_avg_stance * 100, left_avg_initial_swing * 100, left_avg_mid_swing * 100]
    labels = ['Stance phase', 'Initial swing', 'Mid swing', 'Terminal swing']

    ### task mở rộng 23/12/2024: 
    # --- STARTSTART
     
    # Max của knee_x tại stance ( sau khi đã average các cycle) 
    left_stance_percent = left_avg_stance * 100
    right_stance_percent = right_avg_stance * 100
    if name_of_angle == 'KneeAngles' and type_of_angle == 'X':
        max_left_knee_x_stance= np.max(left_mean_angles_smooth[:int(left_stance_percent)])
        max_right_knee_x_stance = np.max(right_mean_angles_smooth[:int(right_stance_percent)])
        print('Maximum of Left KneeAngles X at stance: ', max_left_knee_x_stance)
        print('Maximum of Right KneeAngles X at stance: ', max_right_knee_x_stance)

    # Max hip_z tại stance ( sau khi đã average các cycle) 
    if name_of_angle == 'HipAngles' and type_of_angle == 'Z':
        max_left_hip_z_stance= np.max(left_mean_angles_smooth[:int(left_stance_percent)])
        max_right_hip_z_stance = np.max(right_mean_angles_smooth[:int(right_stance_percent)])
        print('Maximum of Left HipAngles Z at stance: ', max_left_hip_z_stance)
        print('Maximum of Right HipAngles Z at stance: ', max_right_hip_z_stance)

    # Max pelvis_y tại toàn bộ circle ( sau khi đã average các cycle) 
    if name_of_angle == 'PelvisAngles' and type_of_angle == 'Y':
       max_left= np.max(left_mean_angles_smooth)
       max_right = np.max(right_mean_angles_smooth)
       print('Maximum of Left PelvisAngles Y in whole cycle: ', max_left )
       print('Maximum of Right PelvisAngles Y in whole cycle: ', max_right )

    # Giá trị Ankle_x tại Initial Contact  ( sau khi đã average các cycle) 
    if name_of_angle == 'AnkleAngles' and type_of_angle == 'X':
        left_ankle_x_initial_contact= left_mean_angles_smooth[0]
        right_ankle_x_initial_contact = right_mean_angles_smooth[0]
        print('Left AnkleAngles X at initial contact: ', left_ankle_x_initial_contact)
        print('Right AnkleAngles X at initial contact: ', right_ankle_x_initial_contact)
    # --- END


    plt.figure(figsize=(12, 8))
    
    # Plot smoothed mean angles for left leg
    plt.plot(percentages, left_mean_angles_smooth, label="Average left", color='red', linewidth=2)
    plt.fill_between(percentages, 
                     left_mean_angles_smooth - left_std_angles_smooth, 
                     left_mean_angles_smooth + left_std_angles_smooth, 
                     color='red', alpha=0.2)
    # Plot smoothed mean angles for right leg
    plt.plot(percentages, right_mean_angles_smooth, label="Average right", color='blue', linewidth=2)
    plt.fill_between(percentages, 
                     right_mean_angles_smooth - right_std_angles_smooth, 
                     right_mean_angles_smooth + right_std_angles_smooth, 
                     color='blue', alpha=0.2)

    # Plot phase lines and labels
    for x in left_x_values:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=1.5)
    for x in right_x_values:
        plt.axvline(x=x, color='blue', linestyle='--', linewidth=1.5)

    # Get the lowest y-axis value for placing labels
    y_min = plt.gca().get_ylim()[0]
    # Plot labels at the desired positions
    for pos, label in zip(label_positions, labels):
        plt.text(pos + 0.5, y_min - 0.05 * abs(y_min), label, rotation=90, verticalalignment='bottom', color='red', fontsize=12)
    plt.xlim(-10, 110)
    plt.xlabel('Normalized (percent)', fontsize=15)
    plt.ylabel('Angle (degree)', fontsize=15)
    plt.title(f"{name_of_angle}_{type_of_angle}", fontsize=20)
    plt.xticks(range(0, 101, 10), fontsize=10)
    plt.tick_params(axis='x', which='both', length=5, direction='inout')
    plt.minorticks_on()
    plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))
    plt.tick_params(axis='x', which='minor', length=3, direction='inout')
    plt.grid(True)
    plt.legend()
    output_folder_path = os.path.join(folder_path, 'Chart')
    os.makedirs(output_folder_path, exist_ok=True)
    plot_path = os.path.join(output_folder_path, f"{name_of_angle}_{type_of_angle}.png")
    plt.savefig(plot_path, format="png")
    plt.close()


def save_all(processed_file_path_left,processed_file_path_right,folder_path,MR_file,nexus_file_array,drop_row_in_processed_file):
    name_of_angle = ['AnkleAngles','HipAngles','PelvisAngles','KneeAngles']
    type_of_angle = ['X','Y','Z']
    
    mean_phase_left = pd.read_csv(processed_file_path_left)
    mean_phase_right = pd.read_csv(processed_file_path_right)
 
    for i in name_of_angle:
        for j in type_of_angle:
            #plot mean + std on same chart
            table_of_angle_left = create_table_of_angle(processed_file_path_left,folder_path, MR_file, nexus_file_array,side= 'L' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
            table_of_angle_right = create_table_of_angle(processed_file_path_right,folder_path, MR_file, nexus_file_array,side= 'R' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
            plot_mean_angles_with_phases(folder_path,name_of_angle = i,type_of_angle = j,table_of_angle_left = table_of_angle_left, table_of_angle_right=table_of_angle_right, mean_phase_left=mean_phase_left, mean_phase_right=mean_phase_right)
            #plot all cycle lines
            plot_all_cycle(processed_file_path_left, folder_path, MR_file, nexus_file_array,side= 'L' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
            plot_all_cycle(processed_file_path_right, folder_path, MR_file, nexus_file_array,side= 'R' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)


# code giống bên trên nhưng chỉ dành cho không có Right hay Left, (được mở rộng bắt đầu từ case của Truong Phuc Son 10_12_2024)

def plot_mean_angles_with_phases_2(folder_path, name_of_angle, type_of_angle, table_of_angle, mean_phase):
    # Calculate mean and standard deviation angles across percentages for both legs
    mean_angles, std_angles = calculate_mean_and_std_angles(table_of_angle)
  
    percentages = np.linspace(0, 100, 100)

    # Apply a smoothing filter (moving average)
    left_mean_angles_smooth = uniform_filter1d(mean_angles, size=2)
 
    left_std_angles_smooth = uniform_filter1d(std_angles, size=2)
  
    # Calculate phase means for both legs
    avg_stance, avg_initial_swing, avg_mid_swing = calculate_phase_means(mean_phase)
  
    # Define x values for vertical lines and labels for both legs
    left_x_values = [avg_stance * 100, avg_initial_swing * 100, avg_mid_swing * 100]

    label_positions = [0, avg_stance * 100, avg_initial_swing * 100, avg_mid_swing * 100]
    labels = ['Stance phase', 'Initial swing', 'Mid swing', 'Terminal swing']

    ### task mở rộng 23/12/2024: 

    left_avg_stance, _, _ = calculate_phase_means(mean_phase)
 

    #Average của các giá trị CPD trong toàn bộ stance phase (sau khi đã average các cycle)
    stance_percent = left_avg_stance * 100

    if name_of_angle == 'CPD angle':
        average_of_CPD_stance = np.mean(left_mean_angles_smooth[:int(stance_percent)])
        print('Average of CPD value in stance: ', average_of_CPD_stance)

    plt.figure(figsize=(12, 8))
    
    # Plot smoothed mean angles for left leg
    plt.plot(percentages, left_mean_angles_smooth, label="Average", color='red', linewidth=2)
    plt.fill_between(percentages, 
                     left_mean_angles_smooth - left_std_angles_smooth, 
                     left_mean_angles_smooth + left_std_angles_smooth, 
                     color='red', alpha=0.2)
    # Plot smoothed mean angles for right leg
 

    # Plot phase lines and labels
    for x in left_x_values:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=1.5)
 

    # Get the lowest y-axis value for placing labels
    y_min = plt.gca().get_ylim()[0]
    # Plot labels at the desired positions
    for pos, label in zip(label_positions, labels):
        plt.text(pos + 0.5, y_min - 0.05 * abs(y_min), label, rotation=90, verticalalignment='bottom', color='red', fontsize=12)
    plt.xlim(-10, 110)
    plt.xlabel('Normalized (percent)', fontsize=15)
    plt.ylabel('Angle (degree)', fontsize=15)
    plt.title(f"{name_of_angle}_{type_of_angle}", fontsize=20)
    plt.xticks(range(0, 101, 10), fontsize=10)
    plt.tick_params(axis='x', which='both', length=5, direction='inout')
    plt.minorticks_on()
    plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))
    plt.tick_params(axis='x', which='minor', length=3, direction='inout')
    plt.grid(True)
    plt.legend()
    output_folder_path = os.path.join(folder_path, 'Chart')
    os.makedirs(output_folder_path, exist_ok=True)
    plot_path = os.path.join(output_folder_path, f"{name_of_angle}_{type_of_angle}_mean.png")
    plt.savefig(plot_path, format="png")
    plt.close()

def save_all_2(processed_file_path_left,processed_file_path_right,folder_path,MR_file,nexus_file_array,drop_row_in_processed_file):
    name_of_angle = ['CPD angle','Frontal pelvic tilt','Left Foot angle','Right Foot angle']
    type_of_angle = ['Z']
    
    mean_phase = pd.read_csv(processed_file_path_left)
 
 
    for i in name_of_angle:
        for j in type_of_angle:
            #plot mean + std on same chart
            table_of_angle = create_table_of_angle(processed_file_path_left,folder_path, MR_file, nexus_file_array,side= '' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
            
            plot_mean_angles_with_phases_2(folder_path,name_of_angle = i,type_of_angle = j,table_of_angle = table_of_angle, mean_phase = mean_phase)
            #plot all cycle lines
            plot_all_cycle(processed_file_path_left, folder_path, MR_file, nexus_file_array,side= '' ,name_of_angle= i ,type_of_angle= j,drop_row_in_processed_file=drop_row_in_processed_file)
  