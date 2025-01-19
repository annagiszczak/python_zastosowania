from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
import numpy as np
from scipy.integrate import odeint

# SIR model function
def sir_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

# Simulation function
def simulate_sir(beta, gamma, S0, I0, R0, t_max):
    dt = 0.1
    t = np.arange(0, t_max + dt, dt)
    y0 = [S0, I0, R0]
    solution = odeint(sir_model, y0, t, args=(beta, gamma))
    S, I, R = solution.T
    return S, I, R, t

# Initial parameters
beta = 0.3
gamma = 0.1
S0 = 0.99
I0 = 0.01
R0 = 0.0
t_max = 100

S, I, R, t = simulate_sir(beta, gamma, S0, I0, R0, t_max)

source = ColumnDataSource(data={"t": t, "S": S, "I": I, "R": R})

# Plot
plot = figure(title="SIR Model", x_axis_label="Time", y_axis_label="Population Fraction", height=400, width=700)
plot.line("t", "S", source=source, color="blue", legend_label="Susceptible")
plot.line("t", "I", source=source, color="red", legend_label="Infected")
plot.line("t", "R", source=source, color="green", legend_label="Removed")
plot.legend.location = "right"
plot.grid.grid_line_dash = [6,4]

# Sliders
beta_slider = Slider(title="Beta (Transmission Rate)", value=beta, start=0.05, end=1.0, step=0.01)
gamma_slider = Slider(title="Gamma (Recovery Rate)", value=gamma, start=0.01, end=1.0, step=0.01)
tmax_slider = Slider(title="Simulation Time (Days)", value=t_max, start=10, end=200, step=1)

# Callback
def update(attr, old, new):
    beta = beta_slider.value
    gamma = gamma_slider.value
    t_max = tmax_slider.value
    S, I, R, t = simulate_sir(beta, gamma, S0, I0, R0, t_max)
    source.data = {"t": t, "S": S, "I": I, "R": R}

beta_slider.on_change("value", update)
gamma_slider.on_change("value", update)
tmax_slider.on_change("value", update)

# Layout
dashboard = column(plot, row(beta_slider, gamma_slider, tmax_slider))

curdoc().add_root(dashboard)
curdoc().title = "SIR Model Dashboard"


