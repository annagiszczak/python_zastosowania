import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


'''Celem tego projektu jest sprawdzenie, jak wyglądają równania oscylatora harmonicznego z tłumieniem/wymuszeniem (kosinusoidalnym) i rozwiązanie symboliczne tych dwóch równań. Należy wykonać wykresy dla kilku wartości parametru tłumienia i częstotliwości wymuszenia. Następnie należy rozwiązać równanie z tłumieniem i wymuszeniem i też zrobić wykresy.'''

# const
t = sp.symbols('t', real=True)
x = sp.Function('x')(t)
gamma, omega_0, F_0, omega_d = sp.symbols('gamma omega_0 F_0 omega_d', real=True, positive=True)

# Równanie oscylatora z tłumieniem i wymuszeniem
equation = sp.Eq(x.diff(t,2)+omega_0**2*x,0)
# equation = sp.Eq(x.diff(t, 2) + 2 * gamma * x.diff(t) + omega_0**2 * x, F_0 * sp.cos(omega_d * t))


x0 = 1
v0 = 0
t_time = np.linspace(0, 10, 1000)
solution = sp.dsolve(equation, x, ics={x.subs(t, 0): x0, x.diff(t).subs(t, 0): v0})
x_t = solution.rhs

print("Symboliczne rozwiązanie równania:")
sp.pprint(x_t)

params = {
    omega_0: 1.0
}

x_t_specific = x_t.subs(params)
print(x_t_specific)

t = np.linspace(0, 10, 1000)



# #stwórz x i t
# t = [0,3,6]
# x = sp.lambdify(t, x_t_specific, 'numpy')
# x_vals = x(t)
# plt.plot(t, x_vals)
# plt.show()
# x_t_numeric = sp.lambdify(t, x_t.subs({
#     omega_0: omega_0_val
# }), 'numpy')
# # # Funkcja do obliczeń numerycznych
# # x_t_numeric = sp.lambdify(t, x_t.subs({
# #     gamma: gamma_val,
# #     omega_0: omega_0_val,
# #     F_0: F_0_val,
# #     omega_d: omega_d_val
# # }), 'numpy')

# # # Czas do rysowania wykresu
# t_vals = np.linspace(0, 50, 1000)
# x_vals = x_t_numeric(t_vals)
# print(x_vals)
# # # Wykres
# plt.figure(figsize=(10, 6))
# plt.plot(t_vals, x_vals)
# plt.title("Oscylator harmoniczny z tłumieniem i wymuszeniem (symboliczne rozwiązanie)")
# plt.xlabel("Czas $t$")
# plt.ylabel("Przemieszczenie $x(t)$")
# plt.legend()
# plt.grid()
# plt.show()
