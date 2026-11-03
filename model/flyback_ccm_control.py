import numpy as np
import matplotlib.pyplot as plt
import control

PLOT_CURRENT_LOOP = False
PLOT_VOLTAGE_LOOP = False
PLOT_OUTPUT_CURRENT_LOOP = True

FSTART = 1
FEND = 250E3

freq_range = np.geomspace(FSTART, FEND, 1000) * 2*np.pi


#generate plant transfer function

C_OUT = 680E-6
C_OUT_ESR = 0.1

TRANSFORMER_RATIO = 0.5 #NS/NP
TRANSFORMER_INDUCTANCE = 127E-6

R_OUT = 3.0

VIN = 12.0 
VOUT = 5.0 

Rs = 0.7
SENSE_GAIN = 3 

FSW = 250E3 

DUTY_CYCLE = VOUT/(VIN*TRANSFORMER_RATIO + VOUT)
Ri = Rs*SENSE_GAIN

Vslope = VOUT*Ri/(TRANSFORMER_INDUCTANCE*FSW*TRANSFORMER_RATIO)

Km = (VIN+VOUT/TRANSFORMER_RATIO)/Vslope 

Avc = R_OUT*(1-DUTY_CYCLE)/((1+DUTY_CYCLE)*Ri*TRANSFORMER_RATIO)

#poles
Wp1 = (1+DUTY_CYCLE)/(C_OUT*R_OUT) 
Wp2 = Km*Ri/TRANSFORMER_INDUCTANCE

#zeros
Wz1 = 1/(C_OUT*C_OUT_ESR)

#right hand plane zeros
Wrz1 = R_OUT*(1-DUTY_CYCLE)**2 /(TRANSFORMER_INDUCTANCE*DUTY_CYCLE*TRANSFORMER_RATIO**2)

plant_TF = Avc * control.tf([-1/Wrz1, 1], [1/Wp1, 1]) * control.tf([1/Wz1, 1], [1/Wp2, 1])

print(Wp1)
print(Wp2)
print(Wz1)
print(Wrz1)
print(DUTY_CYCLE)

mag,phase,omega = control.bode(plant_TF, freq_range, Hz=True, dB=True, initial_phase=0)
plt.show()

#generate compensator transfer function

R_PULLDOWN = 1E3
R_LED = 330.0
OPTO_CTR = 1.82

C_FB = 220E-9 
C_OPTO = 40E-9

R_FB = 3E3

#zeros
Wz1 = 1/(R_FB*C_FB)

#poles 
Wp1 = 1/(R_FB*C_FB) #pole at origin
Wp2 = 1/(R_PULLDOWN*C_OPTO)

G0 = OPTO_CTR * R_PULLDOWN / R_LED

print(Wz1)
print(Wp1)
print(Wp2)
print(G0)

compensator_TF = G0 * control.tf([1/Wz1, 1], [1/Wp2, 1]) * control.tf([1], [1/Wp1, 0])

mag,phase,omega = control.bode(compensator_TF, freq_range, Hz=True, dB=True, initial_phase=0)
plt.show()


open_loop_TF = compensator_TF * plant_TF
mag,phase,omega = control.bode(open_loop_TF, freq_range, Hz=True, dB=True, initial_phase=0)
plt.show()

