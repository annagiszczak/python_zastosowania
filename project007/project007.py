import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import argparse
import pandas as pd
from matplotlib.animation import FuncAnimation
import IPython.display as display

def sir_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

def simulate_sir(beta, gamma, S0, I0, R0, t_max):
    
    dt = 0.1 
    t = np.arange(0, t_max + dt, dt)

    # Initial conditions
    y0 = [S0, I0, R0]

    # Solve ODE
    solution = odeint(sir_model, y0, t, args=(beta, gamma))
    S, I, R = solution.T

    return S, I, R, t

def plot_sir(t, S, I, R):
    plt.figure(figsize=(10, 6))
    plt.plot(t, S, label='Susceptible', color='blue')
    plt.plot(t, I, label='Infected', color='red')
    plt.plot(t, R, label='Removed', color='green')
    plt.xlabel('Time')
    plt.ylabel('Population Fraction')
    plt.title('SIR Model Simulation: gamma = 0.9')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":

    #constants 1 
    beta = 0.3
    gamma = 0.1
    S0 = 0.99
    I0 = 0.01
    R0 = 0.0
    t_max = 100

    S, I, R, t = simulate_sir(beta, gamma, S0, I0, R0, t_max)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(t, S, label='Susceptible', color='blue')
    plt.plot(t, I, label='Infected', color='red')
    plt.plot(t, R, label='Removed', color='green')
    plt.xlabel('Time')
    plt.ylabel('Population Fraction')
    plt.title('SIR Model Simulation')
    plt.legend()
    plt.grid()
    plt.show()

    gamma =  0.9
    S, I, R, t = simulate_sir(beta, gamma, S0, I0, R0, t_max)
    plot_sir(t, S, I, R)

    

    #animation if beta is changing

    # fig = plt.figure(figsize=(10, 6))
    # fig.set_tight_layout(True)

    # ax = plt.subplot()
    # line1, = ax.plot([], [], 'C1--', lw=2)
    # ax.set_xlim(0, t_max)
    # ax.set_ylim(0, 1)

    # plt.close()

    # def animation_frame(i):
    #     line1.set_data(t[:i], R[:i])
    #     return line1,

    # ani = FuncAnimation(fig, animation_frame, frames=len(t), interval = 40, blit=True)
    # # display(ani.to_jshtml())
    # ani.save('sir_animation.gif', writer='pillow', fps=20)
        