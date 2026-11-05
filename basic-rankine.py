from iapws import IAPWS95

# fixed parameters
Q_h = 1000
P_high = 6
T_3 = 275.6 + 273.15
T_4 = 41.5 + 273.15
P_low = 0.008


# Isentropic compression in pump
cooled_liquid = IAPWS95(T=T_4, x=0, P=P_low)
h1 = cooled_liquid.h
v_water = cooled_liquid.rho/1000

w_P = v_water*(P_high - P_low)   # Pump work
h2 = h1 + w_P

# calculate mass_flow
saturated_vapor = IAPWS95(T=T_3,x=1,P=P_high)
h3 = saturated_vapor.h

m = Q_h/(h2-h3)   # mass flow

# calculate output power
s3 = saturated_vapor.s
condensed_vapor = IAPWS95(s = s3, P=P_low)
x = condensed_vapor.x
h4 = condensed_vapor.h

W_T = (h4-h3)*m   # turbine work

eff = (W_T - w_P * m)/Q_h

print('Output power: %d W' % W_T)
print(f'efficiency: {eff:.0%}')