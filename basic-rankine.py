from iapws import IAPWS95


Q_h = 1000
P_high = 6
T_3 = 275.6 + 273.15
T_4 = 41.5 + 273.15
P_low = 0.008


# Isentropic compression in pump
cooled_liquid = IAPWS95(T=T_4, x=0, P=P_low)
h1 = cooled_liquid.h
v_water = cooled_liquid.rho/1000

h2 = h1 + v_water*(P_high - P_low)


# calculate mass_flow
saturated_vapor = IAPWS95(T=T_3,x=1,P=P_high)
h3 = saturated_vapor.h

m = (h2-h3)/Q_h

# calculate outputpower

s3 = saturated_vapor.s

condensed_vapor = IAPWS95(s = s3, P=P_low)
x = condensed_vapor.x
h4 = condensed_vapor.h

W_T = (h4-h3)*m

print('Output power: ',W_T)