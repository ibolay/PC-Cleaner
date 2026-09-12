import os
import shutil
import tkinter as tk


# =========================
# TEMPORARY FILES
# =========================

def open_temp_folder():
    temp_folder = os.environ.get("TEMP")

    if temp_folder and os.path.exists(temp_folder):
        os.startfile(temp_folder)


def clean_temp():
    temp_folder = os.environ.get("TEMP")

    if not temp_folder or not os.path.exists(temp_folder):
        result_label.config(text="Temporary folder was not found.")
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

    update_temp_size()


# =========================
# SIZE CALCULATION
# =========================

def get_temp_size():
    temp_folder = os.environ.get("TEMP")

    if not temp_folder or not os.path.exists(temp_folder):
        return 0

    total_size = 0

    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            path = os.path.join(root, file)

            try:
                total_size += os.path.getsize(path)
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


def update_temp_size():
    size = get_temp_size()

    size_label.config(
        text=f"Potential space to free: {format_size(size)}"
    )


# =========================
# WINDOWS CACHE
# =========================

def get_windows_cache_folder():
    local_app_data = os.environ.get("LOCALAPPDATA")

    if not local_app_data:
        return None

    return os.path.join(
        local_app_data,
        "Microsoft",
        "Windows",
        "INetCache"
    )


def open_windows_cache_folder():
    cache_folder = get_windows_cache_folder()

    if cache_folder and os.path.exists(cache_folder):
        os.startfile(cache_folder)


def clean_windows_cache():
    cache_folder = get_windows_cache_folder()

    if not cache_folder or not os.path.exists(cache_folder):
        windows_cache_result.config(
            text="Windows cache folder was not found."
        )
        return

    deleted_files = 0
    deleted_folders = 0

    for item in os.listdir(cache_folder):
        path = os.path.join(cache_folder, item)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                deleted_files += 1

            elif os.path.isdir(path):
                shutil.rmtree(path)
                deleted_folders += 1

        except (PermissionError, OSError):
            continue

    windows_cache_result.config(
        text=(
            f"Cleanup completed!\n"
            f"Files removed: {deleted_files}   "
            f"Folders removed: {deleted_folders}"
        )
    )


# =========================
# BROWSER CACHE
# =========================

def get_browser_cache_paths():
    local_app_data = os.environ.get("LOCALAPPDATA")

    if not local_app_data:
        return {}

    return {
        "Chrome": os.path.join(
            local_app_data,
            "Google",
            "Chrome",
            "User Data",
            "Default",
            "Cache"
        ),

        "Edge": os.path.join(
            local_app_data,
            "Microsoft",
            "Edge",
            "User Data",
            "Default",
            "Cache"
        ),

        "Firefox": os.path.join(
            local_app_data,
            "Mozilla",
            "Firefox",
            "Profiles"
        )
    }


def clean_browser_cache():
    browser_paths = get_browser_cache_paths()

    deleted_files = 0
    deleted_folders = 0

    for browser, cache_folder in browser_paths.items():

        if not os.path.exists(cache_folder):
            continue

        for item in os.listdir(cache_folder):
            path = os.path.join(cache_folder, item)

            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.remove(path)
                    deleted_files += 1

                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    deleted_folders += 1

            except (PermissionError, OSError):
                continue

    browser_cache_result.config(
        text=(
            f"Cleanup completed!\n"
            f"Files removed: {deleted_files}   "
            f"Folders removed: {deleted_folders}"
        )
    )


# =========================
# CLEAN ALL
# =========================

def get_folder_size(folder):
    total_size = 0

    if not folder or not os.path.exists(folder):
        return 0

    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            try:
                total_size += os.path.getsize(path)
            except (PermissionError, OSError):
                continue

    return total_size


def clean_all():
    temp_size_before = get_folder_size(os.environ.get("TEMP"))

    windows_cache_folder = get_windows_cache_folder()
    windows_cache_size_before = get_folder_size(windows_cache_folder)

    browser_sizes_before = 0

    for browser, cache_folder in get_browser_cache_paths().items():
        browser_sizes_before += get_folder_size(cache_folder)

    total_size_before = (
        temp_size_before
        + windows_cache_size_before
        + browser_sizes_before
    )

    clean_temp()
    clean_windows_cache()
    clean_browser_cache()

    temp_size_after = get_folder_size(os.environ.get("TEMP"))

    windows_cache_size_after = get_folder_size(
        get_windows_cache_folder()
    )

    browser_sizes_after = 0

    for browser, cache_folder in get_browser_cache_paths().items():
        browser_sizes_after += get_folder_size(cache_folder)

    total_size_after = (
        temp_size_after
        + windows_cache_size_after
        + browser_sizes_after
    )

    freed_space = total_size_before - total_size_after

    if freed_space < 0:
        freed_space = 0

    update_temp_size()

    status_label.config(
        text=f"Cleanup completed!\n"
             f"Space freed: {format_size(freed_space)}"
    )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("PC Cleaner")
root.geometry("900x650")
root.minsize(800, 550)
root.configure(bg="#f4f6f8")


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg="#ffffff"
)

header.pack(
    fill="x"
)


title_label = tk.Label(
    header,
    text="PC Cleaner",
    font=("Segoe UI", 24, "bold"),
    bg="#ffffff",
    fg="#111827"
)

title_label.pack(
    anchor="w",
    padx=30,
    pady=(25, 2)
)


subtitle_label = tk.Label(
    header,
    text="Clean unnecessary files and keep your PC fresh",
    font=("Segoe UI", 11),
    bg="#ffffff",
    fg="#6b7280"
)

subtitle_label.pack(
    anchor="w",
    padx=30,
    pady=(0, 20)
)


# =========================
# CONTENT
# =========================

content_container = tk.Frame(
    root,
    bg="#f4f6f8"
)

content_container.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=20
)

canvas = tk.Canvas(
    content_container,
    bg="#f4f6f8",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    content_container,
    orient="vertical",
    command=canvas.yview
)

content = tk.Frame(
    canvas,
    bg="#f4f6f8"
)

content.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


canvas.bind_all("<MouseWheel>", on_mouse_wheel)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =========================
# CLEANUP LOCATIONS
# =========================

cleanup_locations = [
    "Temporary Files",
    "Windows Cache",
    "Browser Cache"
]

locations_label = tk.Label(
    content,
    text=f"{len(cleanup_locations)} Cleanup Locations",
    font=("Segoe UI", 11, "bold"),
    bg="#f4f6f8",
    fg="#6b7280"
)

locations_label.pack(
    anchor="w",
    pady=(0, 5)
)


# =========================
# TEMP CARD
# =========================

temp_card = tk.Frame(
    content,
    bg="#ffffff"
)

temp_card.pack(
    fill="x",
    pady=(0, 12)
)


temp_title = tk.Label(
    temp_card,
    text="Temporary Files",
    font=("Segoe UI", 15, "bold"),
    bg="#ffffff",
    fg="#111827"
)

temp_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 3)
)


temp_description = tk.Label(
    temp_card,
    text="Remove unnecessary temporary files from your Windows user folder.",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#6b7280"
)

temp_description.pack(
    anchor="w",
    padx=25
)


size_label = tk.Label(
    temp_card,
    text="Potential space to free: Calculating...",
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#2563eb"
)

size_label.pack(
    anchor="w",
    padx=25,
    pady=(10, 0)
)


temp_buttons = tk.Frame(
    temp_card,
    bg="#ffffff"
)

temp_buttons.pack(
    anchor="w",
    padx=25,
    pady=(15, 10)
)


clean_temp_button = tk.Button(
    temp_buttons,
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

clean_temp_button.pack(
    side="left",
    padx=(0, 10)
)


open_temp_button = tk.Button(
    temp_buttons,
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

open_temp_button.pack(
    side="left"
)


result_label = tk.Label(
    temp_card,
    text="",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#374151",
    justify="left"
)

result_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


# =========================
# WINDOWS CACHE CARD
# =========================

windows_cache_card = tk.Frame(
    content,
    bg="#ffffff"
)

windows_cache_card.pack(
    fill="x",
    pady=(0, 12)
)


windows_cache_title = tk.Label(
    windows_cache_card,
    text="Windows Cache",
    font=("Segoe UI", 15, "bold"),
    bg="#ffffff",
    fg="#111827"
)

windows_cache_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 3)
)


windows_cache_description = tk.Label(
    windows_cache_card,
    text="Remove cached Windows internet files.",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#6b7280"
)

windows_cache_description.pack(
    anchor="w",
    padx=25
)


windows_cache_buttons = tk.Frame(
    windows_cache_card,
    bg="#ffffff"
)

windows_cache_buttons.pack(
    anchor="w",
    padx=25,
    pady=(15, 10)
)


windows_cache_button = tk.Button(
    windows_cache_buttons,
    text="Clean Windows Cache",
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="#ffffff",
    activebackground="#1d4ed8",
    activeforeground="#ffffff",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    command=clean_windows_cache
)

windows_cache_button.pack(
    side="left",
    padx=(0, 10)
)


windows_cache_open_button = tk.Button(
    windows_cache_buttons,
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
    command=open_windows_cache_folder
)

windows_cache_open_button.pack(
    side="left"
)


windows_cache_result = tk.Label(
    windows_cache_card,
    text="",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#374151",
    justify="left"
)

windows_cache_result.pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


# =========================
# BROWSER CACHE CARD
# =========================

def open_browser_cache_folder():
    browser_paths = get_browser_cache_paths()

    for browser, cache_folder in browser_paths.items():
        if os.path.exists(cache_folder):
            os.startfile(cache_folder)
            return

browser_cache_card = tk.Frame(
    content,
    bg="#ffffff"
)

browser_cache_card.pack(
    fill="x",
    pady=(0, 12)
)


browser_cache_title = tk.Label(
    browser_cache_card,
    text="Browser Cache",
    font=("Segoe UI", 15, "bold"),
    bg="#ffffff",
    fg="#111827"
)

browser_cache_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 3)
)


browser_cache_description = tk.Label(
    browser_cache_card,
    text="Clean cached files from Chrome and Microsoft Edge.",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#6b7280"
)

browser_cache_description.pack(
    anchor="w",
    padx=25
)


browser_cache_button = tk.Button(
    browser_cache_card,
    text="Clean Browser Cache",
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="#ffffff",
    activebackground="#1d4ed8",
    activeforeground="#ffffff",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    command=clean_browser_cache
)

browser_cache_open_button = tk.Button(
    browser_cache_card,
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
    command=open_browser_cache_folder
)

browser_cache_open_button.pack(
    anchor="w",
    padx=25,
    pady=(0, 10)
)

browser_cache_button.pack(
    anchor="w",
    padx=25,
    pady=(15, 10)
)


browser_cache_result = tk.Label(
    browser_cache_card,
    text="",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#374151",
    justify="left"
)

browser_cache_result.pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


# =========================
# STATUS
# =========================

status_card = tk.Frame(
    content,
    bg="#ffffff"
)

status_card.pack(
    fill="x",
    pady=(0, 12)
)


status_label = tk.Label(
    status_card,
    text="Ready to clean.",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#6b7280"
)

status_label.pack(
    anchor="w",
    padx=25,
    pady=15
)

# =========================
# REFRESH BUTTON
# =========================

def refresh_all():
    update_temp_size()

    status_label.config(
        text="All cleanup locations refreshed."
    )

refresh_button = tk.Button(
    content,
    text="Refresh",
    font=("Segoe UI", 10, "bold"),
    bg="#e5e7eb",
    fg="#374151",
    activebackground="#d1d5db",
    activeforeground="#111827",
    relief="flat",
    padx=20,
    pady=8,
    cursor="hand2",
    command=refresh_all
)

refresh_button.pack(
    pady=(0, 10)
)

# =========================
# CLEAN ALL BUTTON
# =========================

clean_all_button = tk.Button(
    content,
    text="CLEAN ALL",
    font=("Segoe UI", 12, "bold"),
    bg="#111827",
    fg="#ffffff",
    activebackground="#1f2937",
    activeforeground="#ffffff",
    relief="flat",
    padx=30,
    pady=12,
    cursor="hand2",
    command=clean_all
)

clean_all_button.pack(
    pady=(5, 15)
)


# =========================
# FOOTER
# =========================

footer = tk.Label(
    root,
    text="PC Cleaner • Windows Utility",
    font=("Segoe UI", 9),
    bg="#f4f6f8",
    fg="#9ca3af"
)

footer.pack(
    pady=(0, 10)
)


# =========================
# START
# =========================

update_temp_size()

root.mainloop()
