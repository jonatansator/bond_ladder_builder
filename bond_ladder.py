import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Step 1: Assemble bond ladder
def design_ladder(target_cf, terms, bond_options):
    ladder = []
    unmet_cf = np.array(target_cf, dtype=float)
    horizons = np.array(terms)
    for opt in bond_options:
        yield_rate, duration, value = opt
        if duration in horizons:
            idx = np.where(horizons == duration)[0][0]
            flow = value * yield_rate
            if duration == horizons[-1]:
                flow += value  # Include principal at end
            bond_count = min(unmet_cf[idx] / flow, 1)
            if bond_count > 0:
                ladder.append((yield_rate, duration, value, bond_count))
                unmet_cf[idx] -= bond_count * flow
    return ladder, unmet_cf

# Step 2: Compute and visualize ladder
def update_ladder():
    try:
        cf_text = e_cf.get().split(",")
        term_text = e_term.get().split(",")
        df = [float(x.strip()) for x in cf_text]
        tt = [int(t.strip()) for t in term_text]
        
        bonds = []
        for i in range(3):
            y = e_yield[i].get()
            d = e_dur[i].get()
            v = e_val[i].get()
            if y and d and v:
                bonds.append((float(y), int(d), float(v)))
        
        if len(df) != len(tt):
            raise ValueError("Cash flows and terms must align in number")
        if any(x <= 0 for x in df) or any(t <= 0 for t in tt):
            raise ValueError("All inputs must be positive")
        if not bonds:
            raise ValueError("Provide at least one bond option")
        if any(b[0] < 0 or b[1] <= 0 or b[2] <= 0 for b in bonds):
            raise ValueError("Bond details must be positive")
        
        ladder, leftover = design_ladder(df, tt, bonds)
        
        lbl_ladder.config(text=f"Bond Ladder Size: {len(ladder)}")
        lbl_unmet.config(text=f"Unmet Cash Flow: {sum(leftover):.2f}")
        
        XX = np.array(tt)
        orig_cf = np.array(df)
        matched_cf = orig_cf - leftover
        
        ax.clear()
        ax.bar(XX - 0.2, orig_cf, width=0.4, label='Desired Cash Flows', color='#FF6B6B')
        ax.bar(XX + 0.2, matched_cf, width=0.4, label='Matched by Ladder', color='#4ECDC4')
        ax.set_xlabel('Maturity (Years)', color='white')
        ax.set_ylabel('Cash Flow ($)', color='white')
        ax.set_title('Bond Ladder Builder', color='white')
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.5)
        ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
        ax.tick_params(colors='white')
        canv.draw()
    
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Critical error: {str(e)}")

# Step 3: Configure GUI
root = tk.Tk()
root.title("Bond Ladder Builder")
root.configure(bg='#1E1E1E')

frm = ttk.Frame(root, padding=10)
frm.pack()
frm.configure(style='Dark.TFrame')

# Step 4: Initialize plot
fig, ax = plt.subplots(figsize=(7, 5))
canv = FigureCanvasTkAgg(fig, master=frm)
canv.get_tk_widget().pack(side=tk.LEFT)

# Step 5: Set up controls
ctrl = ttk.Frame(frm)
ctrl.pack(side=tk.RIGHT, padx=10)
ctrl.configure(style='Dark.TFrame')

style = ttk.Style()
style.theme_use('default')
style.configure('Dark.TFrame', background='#1E1E1E')
style.configure('Dark.TLabel', background='#1E1E1E', foreground='white')
style.configure('TButton', background='#333333', foreground='white')
style.configure('TEntry', fieldbackground='#333333', foreground='white')

ttk.Label(ctrl, text="Desired CF ($):", style='Dark.TLabel').pack(pady=3)
e_cf = ttk.Entry(ctrl); e_cf.pack(pady=3); e_cf.insert(0, "1000, 2000, 3000")
ttk.Label(ctrl, text="Maturity Dates:", style='Dark.TLabel').pack(pady=3)
e_term = ttk.Entry(ctrl); e_term.pack(pady=3); e_term.insert(0, "1, 2, 3")

ttk.Label(ctrl, text="Bond Choices:", style='Dark.TLabel').pack(pady=5)
e_yield = []
e_dur = []
e_val = []
bond_defaults = [(0.03, 1, 1000), (0.04, 2, 980), (0.05, 3, 950)]

for i in range(3):
    bf = ttk.Frame(ctrl)
    bf.pack(pady=2)
    ttk.Label(bf, text=f"Bond {i+1}:", style='Dark.TLabel').pack(side=tk.LEFT)
    yld = ttk.Entry(bf, width=5); yld.pack(side=tk.LEFT, padx=2)
    dur = ttk.Entry(bf, width=5); dur.pack(side=tk.LEFT, padx=2)
    val = ttk.Entry(bf, width=7); val.pack(side=tk.LEFT, padx=2)
    yld.insert(0, str(bond_defaults[i][0]))
    dur.insert(0, str(bond_defaults[i][1]))
    val.insert(0, str(bond_defaults[i][2]))
    e_yield.append(yld)
    e_dur.append(dur)
    e_val.append(val)

ttk.Button(ctrl, text="Build Ladder", command=update_ladder).pack(pady=10)
lbl_ladder = ttk.Label(ctrl, text="Bond Ladder Size: ", style='Dark.TLabel'); lbl_ladder.pack(pady=2)
lbl_unmet = ttk.Label(ctrl, text="Unmet Cash Flow: ", style='Dark.TLabel'); lbl_unmet.pack(pady=2)

# Step 6: Start application
update_ladder()
root.mainloop()