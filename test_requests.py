import requests

r = requests.get("http://127.0.0.1:8050/api", params={"raw": "employee_ID, distance_in_m, time_in_s, CO2_in_g\n12, 2760, 1692, 31678\n14, 1223, 983, 8907\n17, 610, 562, 1762\n18, 456, 672, 671\n19, 32908, 5427, 59871"})
print(r.url)
print(r.text)
