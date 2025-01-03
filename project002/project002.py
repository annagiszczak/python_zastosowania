import sys
import argparse
import rich
from rich.progress import track
import rich.traceback
from ascii_graph import Pyasciigraph
from ascii_graph import colors
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

'''
Mierzenie wykonania programu
'''
import time
start_time = time.time()

import numpy as np
from PIL import Image

from collections import defaultdict
from PIL import Image, ImageDraw

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable



rich.traceback.install()
rich.get_console().clear()
rich.get_console().rule(":raccoon: :raccoon: :raccoon: ISING :raccoon: :raccoon: :raccoon:", style="bold magenta")

parser = argparse.ArgumentParser(description="Analysis of words number")
parser.add_argument('--number', '-n', type=int, default=10, help="Size of net  (default 10).", required = True)
parser.add_argument('--j_value', '-J', type=float, default=1, help="Value of J (default 1)", required = True)
parser.add_argument('--beta','-b', type=float, default=1, help="Value of Beta (default 1).", required = True)
parser.add_argument('--B_value','-B', type=float, default=1, help="Value of B (default 1).", required = True)
parser.add_argument('--steps','-s', type=int, default=100, help="Macro step (default 100).", required = True)
parser.add_argument('--density','-d', type=float, default=0.5, help="density (default 0.5).")
parser.add_argument('--image_prefix','-ip', type=str, default='./picture/', help="Picture path (default ./picture).")
parser.add_argument('--animation_file','-af', type=str, default='animation.gif', help="animation name (default 'animation.gif).")
parser.add_argument('--magnetization_file','-mf', type=str, default='magnet.txt', help="magnet file(default 'magnet.txt).")



class IsingModel:
    def __init__(self, args):
        self.n = args.number
        self.J = args.j_value
        self.beta = args.beta
        self.B = args.B_value
        self.steps = args.steps
        self.spin_density = args.density
        self.image_prefix = args.image_prefix  
        self.animation_file = args.animation_file 
        self.magnetization_file = args.magnetization_file 

        self.grid = np.random.choice([-1, 1], size=(self.n, self.n), p=[1 - args.density, args.density])
        self.magnetization = []

    def energy_change(self, i, j):
        """Oblicza zmianę energii przy flippowaniu spinu na pozycji (i, j)."""
        spin = self.grid[i, j]
        neighbors = (
            self.grid[(i+1) % self.n, j] + self.grid[(i-1) % self.n, j] +
            self.grid[i, (j+1) % self.n] + self.grid[i, (j-1) % self.n]
        )
        dE = 2 * spin * (self.J * neighbors + self.B)
        return dE

    def monte_carlo_step(self):
        """Wykonuje jeden makrokrok Monte Carlo."""
        for _ in range(self.n * self.n):
            i, j = np.random.randint(0, self.n, size=2)
            dE = self.energy_change(i, j)
            if dE < 0 or np.random.rand() < np.exp(-self.beta * dE):
                self.grid[i, j] *= -1

    def simulate(self):
            """Uruchamia symulację, zapisuje magnetyzację i generuje obrazy oraz animację."""
            images = []
            for step in track(range(self.steps), description="Running Monte Carlo simulation"):
                self.monte_carlo_step()
                magnetization = np.sum(self.grid) / (self.n * self.n)
                self.magnetization.append(magnetization)

                if self.image_prefix:
                    image = Image.new('RGB', (self.n, self.n), 'pink')
                    draw = ImageDraw.Draw(image)
                    for i in range(self.n):
                        for j in range(self.n):
                            color = (90, 172, 207) if self.grid[i, j] == 1 else (128, 194, 113)
                            draw.point((j, i), fill=color)
                    image = image.resize((self.n * 100, self.n * 100), Image.NEAREST)
                    image.save(f"{self.image_prefix}_{step}.png")
                    images.append(image)

            if self.animation_file:
                images[0].save(
                self.animation_file,
                save_all=True,
                append_images=images[1:],
                duration=100,
                loop=0
                )
            #     imageio.mimsave(self.animation_file, [np.array(img) for img in images], fps=10)

            if self.magnetization_file:
                with open(self.magnetization_file, 'w') as f:
                    for step, m in enumerate(self.magnetization):
                        f.write(f"{step}\t{m}\n")

args = parser.parse_args()
ising = IsingModel(args)
ising.simulate()
rich.get_console().rule(":raccoon: :raccoon: :raccoon: DONE! :raccoon: :raccoon: :raccoon:", style="bold magenta")
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Czas wykonania: {elapsed_time:.6f} sekund")