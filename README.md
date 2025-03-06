# Bond Ladder Builder

- This project creates a bond ladder to match desired cash flows using a graphical user interface (GUI) built with Tkinter and Matplotlib.
- It allows users to input target cash flows, maturity terms, and bond options, then visualizes the results.

---

## Files
- `bond_ladder.py`: Main script for designing and visualizing the bond ladder.
- `output.png`: Plot.

---

## Libraries Used
- `numpy`
- `matplotlib`
- `tkinter`
- `matplotlib.backends.backend_tkagg`

---

## Features
- **Input**: 
  - Desired cash flows (comma-separated values in dollars)
  - Maturity terms (comma-separated years)
  - Up to 3 bond options (yield rate, duration, and face value)
- **Output**: 
  - Calculates a bond ladder to meet cash flow targets
  - Displays a bar chart comparing desired vs. matched cash flows
  - Shows the number of bonds in the ladder and total unmet cash flow

