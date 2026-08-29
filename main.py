import os
import shutil
import tkinter as tk

def open_temp_folder():
    temp_folder = os.environ.get("TEMP")

    if temp_folder and os.path.exists(temp_folder):
        os.startfile(temp_folder)

def clean_temp():
    temp_folder = os.environ.get("TEMP")

    if not temp_folder or not os.path.exists(temp_folder):
        result_label.config(text="Temp folder was not found.")
        return

    deleted_files = 0
    deleted_folders = 0

    for item in os.listdir(temp_folder):
        path = os.path.join(temp_folder, item)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                deleted_files += 1

            elif os.path.isdir(path):
                shutil.rmtree(path)
                deleted_folders += 1

        except (PermissionError, OSError):
            continue

    result_label.config(
        text=(
            "Cleanup completed!\n\n"
            f"Files removed: {deleted_files}\n"
            f"Folders removed: {deleted_folders}"
        )
    )


root = tk.Tk()
root.title("PC Cleaner")
root.geometry("800x600")

title = tk.Label(
    root,
    text="PC Cleaner",
    font=("Segoe UI", 24, "bold")
)

title.pack(pady=30)

clean_button = tk.Button(
    root,
    text="Clean Temp Files",
    font=("Segoe UI", 12, "bold"),
    command=clean_temp
)

clean_button.pack(pady=20)

open_button = tk.Button(
    root,
    text="Open Temp Folder",
    font=("Segoe UI", 12),
    command=open_temp_folder
)

open_button.pack(pady=10)

result_label = tk.Label(
    root,
    text="Ready to clean.",
    font=("Segoe UI", 12)
)

result_label.pack(pady=20)

root.mainloop()