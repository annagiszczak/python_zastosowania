import argparse
import numpy as np
from PIL import Image, ImageDraw
from rich.progress import track
from numba import njit
from rich.progress import track
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor
import rich
import rich.traceback
import numba
from numba import types, typed

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

rich.traceback.install()
rich.get_console().clear()
rich.get_console().rule(":raccoon: :raccoon: :raccoon: ISING :raccoon: :raccoon: :raccoon:", style="bold magenta")

def initialize_grid(n, spin_density):
    return np.random.choice([-1, 1], size=(n, n), p=[1 - spin_density, spin_density])

@njit
def energy_change(grid, i, j, J, B, n):
    spin = grid[i, j]
    neighbors = (
        grid[(i+1) % n, j] + grid[(i-1) % n, j] +
        grid[i, (j+1) % n] + grid[i, (j-1) % n]
    )
    dE = 2 * spin * (J * neighbors + B)
    return dE

@njit
def monte_carlo_step(grid, n, beta, J, B):
    for _ in range(n * n):
        i, j = np.random.randint(0, n, size=2)
        dE = energy_change(grid, i, j, J, B, n)
        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            grid[i, j] *= -1
    return grid
@njit
def save_image(grid, n, step, image_prefix):
    image = Image.new('RGB', (n, n), 'pink')
    draw = ImageDraw.Draw(image)
    for i in range(n):
        for j in range(n):
            color = (90, 172, 207) if grid[i, j] == 1 else (128, 194, 113)
            draw.point((j, i), fill=color)
    image = image.resize((n * 100, n * 100), Image.NEAREST)
    image.save(f"{image_prefix}_{step}.png")
    return image

def simulate(args):
    n = args.number
    J = args.j_value
    beta = args.beta
    B = args.B_value
    steps = args.steps
    spin_density = args.density
    image_prefix = args.image_prefix
    animation_file = args.animation_file
    magnetization_file = args.magnetization_file

    grid = initialize_grid(n, spin_density)
    magnetization = []
    images = []

    for step in track(range(steps), description="Running Monte Carlo simulation"):
        grid = monte_carlo_step(grid, n, beta, J, B)
        mag = np.sum(grid) / (n * n)
        magnetization.append(mag)

        if image_prefix:
            image = save_image(grid, n, step, image_prefix)
            images.append(image)

    if animation_file:
        images[0].save(
            animation_file,
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0
        )

    if magnetization_file:
        with open(magnetization_file, 'w') as f:
            for step, m in enumerate(magnetization):
                f.write(f"{step}\t{m}\n")

parser = argparse.ArgumentParser(description="Analysis of words number")
parser.add_argument('--number', '-n', type=int, default=10, help="Size of net  (default 10).", required=True)
parser.add_argument('--j_value', '-J', type=float, default=1, help="Value of J (default 1)", required=True)
parser.add_argument('--beta', '-b', type=float, default=1, help="Value of Beta (default 1).", required=True)
parser.add_argument('--B_value', '-B', type=float, default=1, help="Value of B (default 1).", required=True)
parser.add_argument('--steps', '-s', type=int, default=100, help="Macro step (default 100).", required=True)
parser.add_argument('--density', '-d', type=float, default=0.5, help="density (default 0.5).")
parser.add_argument('--image_prefix', '-ip', type=str, default='./picture/', help="Picture path (default ./picture).")
parser.add_argument('--animation_file', '-af', type=str, default='animation.gif', help="animation name (default 'animation.gif).")
parser.add_argument('--magnetization_file', '-mf', type=str, default='magnet.txt', help="magnet file(default 'magnet.txt).")

args = parser.parse_args()
simulate(args)
