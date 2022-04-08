import numpy as np
import pandas as pd
from time import time
from random import choices, seed, randint


# 7g/Km for electric bikes
# 5g/Km for classic bikes
# (https://www.bikeradar.com/features/long-reads/cycling-environmental-impact/#:~:text=Adding%20the%2016g%20per%20kilometre,emissions%20come%20from%20food%20production.)
# 122.3 g CO2/km for cars (average) (https://www.eea.europa.eu/ims/co2-performance-of-new-passenger)
#
# LA STIB
# Metro: 20 gr CO2 /(km*passenger)
# Tram: 30 gr CO2 /(km*passenger)
# Bus: 110 gr CO2 /(km*passenger)
# Train (SNCB): 26 gr CO2 /(km*passenger)
def generate_bike(distance, employees, i):
    avg_speed = np.random.normal(15, 1, 1) / 3.6
    row = {"employee_ID": i, "distance_in_m": distance, "time_in_s": distance / avg_speed,
           "CO2_in_g": 5 * distance / 1000, "category": "bike"}
    employees = pd.concat([employees, pd.DataFrame(row)])
    return employees


def generate_public(distance, employees, i):
    avg_speed = np.random.normal(50, 5, 1) / 3.6
    row = {"employee_ID": i, "distance_in_m": distance, "time_in_s": 2 * distance / avg_speed,
           "CO2_in_g": 50 * distance / 1000, "category": "public"}
    employees = pd.concat([employees, pd.DataFrame(row)])
    return employees


def generate_car(distance, employees, i):
    avg_speed = np.random.normal(50, 5, 1) / 3.6
    row = {"employee_ID": i, "distance_in_m": distance, "time_in_s": distance / avg_speed,
           "CO2_in_g": 122.3 * distance / 1000, "category": "car"}
    employees = pd.concat([employees, pd.DataFrame(row)])
    return employees


def generate_employee(distance, transport_mean, employees, i):
    transport_mean = transport_mean[0]
    if transport_mean == "bike":
        employees = generate_bike(distance, employees, i)
    elif transport_mean == "public transport":
        employees = generate_public(distance, employees, i)
    else:
        employees = generate_car(distance, employees, i)
    return employees


def generate_internal(employees, i):
    distance = abs(np.random.normal(3.6, 0.3, 1)) * 1000
    transport_mean = choices(["bike", "public transport", "car"], weights=(3.2, 42.4, 37.5), k=1)
    return generate_employee(distance, transport_mean, employees, i)


def generate_inbound(employees, i):
    distance = abs(np.random.normal(35, 5, 1)) * 1000
    transport_mean = choices(["bike", "public transport", "car"], weights=(0.7, 43.6, 49.6), k=1)
    return generate_employee(distance, transport_mean, employees, i)


def data_generator(scale_factor=1):
    seed(time())
    total_employee = 100 * scale_factor
    employees = pd.DataFrame()
    for i in range(int(total_employee)):
        if randint(1, 2) == 1:
            employees = generate_internal(employees, i)
        else:
            employees = generate_inbound(employees, i)
    employees.to_csv(f"data/employees_{scale_factor}.csv", index=False)


if __name__ == "__main__":
    data_generator()
