from iapws import IAPWS95
import numpy as np
import matplotlib.pyplot as plt


class rankineCycle:
    def __init__(self, Q_H, T_H):
        self.Q_h = Q_H
        # Initial temperature
        self.T_H = T_H
        # fixed parameters
        self.P_high = 6
        self.T_3 = 275.6 + 273.15
        self.T_4 = 41.5 + 273.15
        self.P_low = 0.008
        # Heat exchanger parameters
        self.UA = Q_H/(T_H - self.T_3)
        self.Ceff = 500  # Heat capacity
        # Isentropic compression in pump
        cooled_liquid = IAPWS95(T=self.T_4, x=0, P=self.P_low)
        self.h1 = cooled_liquid.h
        v_water = cooled_liquid.rho/1000

        w_P = v_water*(self.P_high - self.P_low)   # Pump work
        self.h2 = self.h1 + w_P

        # calculate steam generator vapor enthalpy
        saturated_vapor = IAPWS95(T=self.T_3,x=1,P=self.P_high)
        self.h3 = saturated_vapor.h

        # calculate output power
        s3 = saturated_vapor.s
        condensed_vapor = IAPWS95(s = s3, P=self.P_low)
        #x = condensed_vapor.x
        self.h4 = condensed_vapor.h


        self.m = self.Q_h/(self.h3-self.h2)   # mass flow
        self.w_T = -(self.h4-self.h3)*self.m   # turbine work

    def step(self,dt,Q_h):
        Q_steam = self.UA * (self.T_H - self.T_3)
        print(Q_steam)
        self.m = Q_steam/(self.h3-self.h2)
        self.T_H = self.T_H + dt / self.Ceff * (Q_h - Q_steam)
        self.w_T = -(self.h4-self.h3)*self.m
        return [self.m, self.T_H, self.w_T]

    def simulate(self,Q_plan,dt):
        history = {
            'mass flow': [self.m],
            'heat exchanger temperature': [self.T_H],
            'output power': [self.w_T]
        }
        for Q_h in Q_plan:
            next_vals = self.step(dt,Q_h)
            for i,key in enumerate(history.keys()):
                history[key].append(next_vals[i])

        return history



Q_h = 1000
T_h = 315 + 273.15
dt = 1
steps = 31
Q_plan = np.linspace(1000,995,steps)
time = np.arange(steps)

nuke = rankineCycle(Q_h,T_h)
history = nuke.simulate(Q_plan[1:],dt)
history['reactor power'] = Q_plan
print('Output power: %d W' % nuke.w_T)

fig, axes = plt.subplots(4, 1, sharex=True, figsize=(8, 7))

for ax, key in zip(axes, history):
    ax.plot(time, history[key])
    ax.set_ylabel(key)
    ax.grid(True)

axes[-1].set_xlabel("Time")
fig.tight_layout()
plt.show()