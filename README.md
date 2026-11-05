# Readme

This is a basic thermal modelling excercise for a nuclear power plant with storage.
It will be built in three steps:

1. Steady State Rankine Cycle (assuming PWR)
2. Rankine taking into account thermal inertia
3. PWR with thermal storage

A bonus idea is to do an HTR where the graphite also functions as thermal buffer

## Rankine (steady state)

![Rankine diagram](Rankine-Cycle-scheme.png)

An overview of a basic rankine cycle.

The following parameters for the cycle are chosen:

| Parameter | Value | Unit | Description |
|-|-|-|-|
| Q_H | 1000 | W | Nuclear steam generator input power |
| P_3 | 6 | MPa | Turbine inlet pressure |
| T_3 | 275 | C | Turbine inlet Temperature |
| P_4 | 0.008 | MPa | Turbine outlet pressure |
