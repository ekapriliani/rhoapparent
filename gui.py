import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, messagebox
import backendf as backend


# === GUI SETUP ===
app = ttk.Window(themename="flatly")
app.title("🌍 Visualisasi ERT (ρₐ)")
app.geometry("1100x650")

header = ttk.Frame(app, bootstyle=PRIMARY, padding=10)
header.pack(fill=X)
ttk.Label(header, text="Visualisasi ERT - Resistivitas Semu (ρₐ)",
           font=("Helvetica", 16, "bold"), foreground="white").pack(side=LEFT)

body = ttk.Frame(app)
body.pack(fill=BOTH, expand=True)
sidebar = ttk.Frame(body, width=220, bootstyle=SECONDARY, padding=10)
sidebar.pack(side=LEFT, fill=Y)
content = ttk.Frame(body, bootstyle=LIGHT)
content.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

footer = ttk.Frame(app, padding=5)
footer.pack(fill=X)
status_label = ttk.Label(footer, text="Belum ada data dimuat.", anchor=W)
status_label.pack(side=LEFT, padx=10)

canvas = None
plot_data = None

# === FUNGSI ===
def load_and_plot():
    global canvas, plot_data
    file_path = filedialog.askopenfilename(
        title="Pilih file Excel ERT",
    filetypes=[
    ("All Supported Files", "*.xlsx *.xls *.csv *.txt *.dat *.tsv"),
    ("Excel Files", "*.xlsx *.xls"),
    ("CSV Files", "*.csv"),
    ("Text Files", "*.txt *.dat *.tsv")
])
    if not file_path:
        return

    try:
        metode = metode_var.get() 
        grid_x, grid_z, z_pred, xp, zp, rp = backend.proses_data(file_path, method=metode)

        plot_data = (grid_x, grid_z, z_pred, xp, zp, rp)

        fig, ax = plt.subplots(figsize=(8, 5))
        contour = ax.contourf(grid_x, grid_z, z_pred, cmap=cmap_var.get(), levels=50)
        ax.set_xlabel("Jarak (m)")
        ax.set_ylabel("Kedalaman (m)")
        ax.set_title("Pseudosection Kriging Resistivitas Semu (ρₐ)")
        plt.colorbar(contour, ax=ax, label="ρₐ (Ωm)")

        if canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=content)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        status_label.config(text=f"✅ Grafik berhasil dibuat dari: {os.path.basename(file_path)}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text=f"❌ Gagal memproses: {e}")

def save_plot():
    if not canvas:
        messagebox.showwarning("Tidak ada grafik", "Silakan plot dulu sebelum menyimpan.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
        filetypes=[("PNG Files", "*.png")])
    if file_path:
        canvas.figure.savefig(file_path, dpi=300)
        status_label.config(text=f"💾 Disimpan ke {file_path}")

# === SIDEBAR MENU ===
ttk.Label(sidebar, text="Menu", font=("Helvetica", 13, "bold")).pack(anchor=W, pady=(0, 10))
ttk.Button(sidebar, text="📂 Load & Tampilkan Data", bootstyle=PRIMARY, command=load_and_plot).pack(fill=X, pady=5)
ttk.Button(sidebar, text="💾 Simpan Gambar", bootstyle=SECONDARY, command=save_plot).pack(fill=X, pady=5)

ttk.Label(sidebar, text="Colormap:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(15, 0))
cmap_var = ttk.StringVar(value="viridis")
ttk.Combobox(sidebar, textvariable=cmap_var, values=[
    "jet", "viridis", "plasma", "inferno", "terrain", "cividis"
], bootstyle=INFO).pack(fill=X, pady=5)
ttk.Label(sidebar, text="Metode K:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(15, 0))

metode_var = ttk.StringVar(value="S")
ttk.Combobox(
    sidebar,
    textvariable=metode_var,
    values=["S", "W", "G", "WS"],
    bootstyle=INFO
).pack(fill=X, pady=5)

# === RUN ===
app.mainloop()



