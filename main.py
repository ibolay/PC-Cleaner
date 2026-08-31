import os
import shutil
import tkinter as tk


# -----------------------------
# Functions
# -----------------------------

def open_temp_folder():
    temp_folder = os.environ.get("TEMP")

    if temp_folder and os.path.exists(temp_folder):
        os.startfile(temp_folder)

def get_temp_size():
    temp_folder = os.environ.get("TEMP")

    if not temp_folder or not os.path.exists(temp_folder):
        return 0

    total_size = 0

    for root_dir, dirs, files in os.walk(temp_folder):
        for file in files:
            file_path = os.path.join(root_dir, file)

            try:
                total_size += os.path.getsize(file_path)
            except (PermissionError, OSError):
                continue

    return total_size

def format_size(size):
    if size < 1024:
        return f"{size} B"

    if size < 1024 ** 2:
        return f"{size / 1024:.1f} KB"

    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.1f} MB"

    return f"{size / (1024 ** 3):.2f} GB"

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
            f"Cleanup completed!\n"
            f"Files removed: {deleted_files}   "
            f"Folders removed: {deleted_folders}"
        )
    )


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()
root.title("PC Cleaner")
root.geometry("900x650")
root.minsize(800, 550)
root.configure(bg="#f4f6f8")


# -----------------------------
# Header
# -----------------------------

header = tk.Frame(
    root,
    bg="#ffffff",
    height=100
)

header.pack(fill="x")
header.pack_propagate(False)


title = tk.Label(
    header,
    text="PC Cleaner",
    font=("Segoe UI", 28, "bold"),
    bg="#ffffff",
    fg="#1f2937"
)

title.pack(pady=(18, 0))


subtitle = tk.Label(
    header,
    text="Clean unnecessary files and keep your PC fresh",
    font=("Segoe UI", 11),
    bg="#ffffff",
    fg="#6b7280"
)

subtitle.pack()


# -----------------------------
# Main Content
# -----------------------------

content = tk.Frame(
    root,
    bg="#f4f6f8"
)

content.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=30
)


# -----------------------------
# Temp Cleaner Card
# -----------------------------

temp_card = tk.Frame(
    content,
    bg="#ffffff",
    bd=0,
    highlightthickness=1,
    highlightbackground="#e5e7eb"
)

temp_card.pack(
    fill="x",
    pady=10
)


temp_title = tk.Label(
    temp_card,
    text="Temporary Files",
    font=("Segoe UI", 17, "bold"),
    bg="#ffffff",
    fg="#111827"
)

temp_title.pack(
    anchor="w",
    padx=25,
    pady=(22, 5)
)


temp_description = tk.Label(
    temp_card,
    text="Remove unnecessary temporary files from your Windows user folder.",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#6b7280"
)

size_label = tk.Label(
    temp_card,
    text="Calculating...",
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#2563eb"
)

size_label.pack(
    anchor="w",
    padx=25,
    pady=(8, 0)
)

temp_description.pack(
    anchor="w",
    padx=25
)


# -----------------------------
# Buttons
# -----------------------------

button_frame = tk.Frame(
    temp_card,
    bg="#ffffff"
)

button_frame.pack(
    anchor="w",
    padx=25,
    pady=20
)


clean_button = tk.Button(
    button_frame,
    text="Clean Temp Files",
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="#ffffff",
    activebackground="#1d4ed8",
    activeforeground="#ffffff",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    command=clean_temp
)

clean_button.pack(
    side="left",
    padx=(0, 10)
)


open_button = tk.Button(
    button_frame,
    text="Open Folder",
    font=("Segoe UI", 11),
    bg="#e5e7eb",
    fg="#374151",
    activebackground="#d1d5db",
    activeforeground="#111827",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    command=open_temp_folder
)

open_button.pack(
    side="left"
)


# -----------------------------
# Status
# -----------------------------

status_frame = tk.Frame(
    content,
    bg="#ffffff",
    highlightthickness=1,
    highlightbackground="#e5e7eb"
)

status_frame.pack(
    fill="x",
    pady=(20, 10)
)


status_title = tk.Label(
    status_frame,
    text="Status",
    font=("Segoe UI", 13, "bold"),
    bg="#ffffff",
    fg="#111827"
)

status_title.pack(
    anchor="w",
    padx=25,
    pady=(18, 5)
)


result_label = tk.Label(
    status_frame,
    text="Ready to clean.",
    font=("Segoe UI", 11),
    bg="#ffffff",
    fg="#6b7280"
)

result_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 18)
)


# -----------------------------
# Footer
# -----------------------------

footer = tk.Label(
    root,
    text="PC Cleaner • Windows Utility",
    font=("Segoe UI", 9),
    bg="#f4f6f8",
    fg="#9ca3af"
)

footer.pack(
    pady=(0, 15)
)

def update_temp_size():
    size = get_temp_size()
    size_label.config(
        text=f"Potential space to free: {format_size(size)}"
    )


update_temp_size()

root.mainloop()