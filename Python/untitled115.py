#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:59:26 2024

@author: johnpaulmbagwu
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read the TXT data file containing information about Liquid Water
df_water = pd.read_csv('WATER.TXT', delimiter=' ')

# Extract the stopping power and energy columns from the dataframe
stopping_power_water = df_water['TotalStp.Pow']
energy_water = df_water['KineticEnergy']

# Read the TXT data file containing information about Air
df_air = pd.read_csv('AIR.TXT', delimiter=' ')

# Extract the stopping power and energy columns from the dataframe
stopping_power_air = df_air['TotalStp.Pow']
energy_air = df_air['KineticEnergy']

# Normalize the stopping power to 150 MeV
normalization_energy = 150  # MeV
normalization_index_water = np.where(energy_water == normalization_energy)[0]
normalization_index_air = np.where(energy_air == normalization_energy)[0]

if normalization_index_water.size == 0 or normalization_index_air.size == 0:
    raise ValueError("Normalization energy not found in the data.")

normalized_stopping_power_water = stopping_power_water / stopping_power_water[normalization_index_water].values[0]
normalized_stopping_power_air = stopping_power_air / stopping_power_air[normalization_index_air].values[0]

# Interpolate stopping power data for Air to match the energy values of Water
interpolated_stopping_power_air = np.interp(energy_water, energy_air, normalized_stopping_power_air)

# Calculate the air-to-water stopping power ratio
stopping_power_ratio = interpolated_stopping_power_air / normalized_stopping_power_water

# Plotting
plt.figure(figsize=(10, 6))

# Plotting the air-to-water stopping power ratio
plt.plot(energy_water, stopping_power_ratio, label='Air-to-Water Stopping Power Ratio')

plt.title('Air-to-Water Stopping Power Ratio')
plt.xlabel('Energy (MeV)')
plt.ylabel('Stopping Power Ratio')

# Set the x-axis limits to 1 MeV and 250 MeV
plt.xlim(1, 250)

# Set the y-axis limits for better visibility
plt.ylim(0, max(stopping_power_ratio) * 1.1)

plt.grid(True)
plt.legend()

plt.show()
