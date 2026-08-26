import tkinter as tk


root = tk.Tk()
root.title("PC Cleaner")
root.geometry("800x600")

title = tk.Label(
    root,
    text="PC Cleaner",
    font=("Segoe UI", 24, "bold")
)

title.pack(pady=30)

root.mainloop()