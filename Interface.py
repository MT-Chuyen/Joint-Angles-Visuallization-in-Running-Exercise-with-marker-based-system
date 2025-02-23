import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
import os
from Classify_period import process_file
from Plot_all import save_all,save_all_2


def find_files_with_text(directory, text):
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if text in file:
                matching_files.append(os.path.join(root, file))
    return matching_files

 
def main_function():
    global List_file_run, path_right, path_left,MR3_file ,folder_path  
    # Step 1: Choose a directory using file dialog
    folder_path = filedialog.askdirectory()
    # Step 2: Find the file with "MR3" and get its directory
    for file in os.listdir(folder_path):
        if "MR3" in file and file.endswith(".csv"):
            MR3_file = os.path.join(folder_path, file)
            break
    # Lấy giá trị từ entry, mặc định là None nếu không được nhập
    drop_row_in_processed_file = drop_entry.get()
    if drop_row_in_processed_file.strip():  # Nếu có giá trị, chuyển sang kiểu int
        drop_row_in_processed_file = int(drop_row_in_processed_file)
    else:  # Nếu không, gán mặc định None
        drop_row_in_processed_file = None
        
    process_file(MR3_file)
    processed_right_leg_files = find_files_with_text(folder_path, "__right_leg_processed__")
    if processed_right_leg_files:
        path_right = processed_right_leg_files[0]
    print('path_right : ',path_right)

    processed_left_leg_files = find_files_with_text(folder_path, "__left_leg_processed__")
    if processed_left_leg_files:
        path_left = processed_left_leg_files[0]
    print('path_left:',path_left)
 
    List_file_run = find_files_with_text(folder_path, "running")
    list_file_name = [os.path.basename(file_path) for file_path in List_file_run]
    print(list_file_name)

    save_all(processed_file_path_left= path_left,processed_file_path_right =path_right,folder_path=folder_path,MR_file = MR3_file,nexus_file_array=list_file_name,drop_row_in_processed_file=drop_row_in_processed_file)
    save_all_2(processed_file_path_left= path_left,processed_file_path_right =path_right,folder_path=folder_path,MR_file = MR3_file,nexus_file_array=list_file_name,drop_row_in_processed_file=drop_row_in_processed_file)

# Create the main window
window = tk.Tk()
window.title("Select folder contain dataset")   
window.geometry("400x300")
window.configure(bg="#f0f0f0")   
main_frame = tk.Frame(window, bg="#f0f0f0")
main_frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
drop_label = tk.Label(main_frame, text="Enter row that should be dropped:", font=("Arial", 12), bg="#f0f0f0")
drop_label.pack(pady=(20, 10))   
drop_entry = tk.Entry(main_frame, font=("Arial", 12), width=20)
drop_entry.pack(pady=10)
button_select_file = tk.Button(main_frame, text="Select The Folder", command=main_function, 
                               font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", bd=3)
button_select_file.pack(pady=15)
window.mainloop()
 