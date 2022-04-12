# EmployeeSegmentaion

EmployeeSegmentation is a python app that categorizes the means of transport (car, public transport and bike) used by different employees.

It uses Dash and Flask for the webApp and the API. The server is managed by Waitress.

## Prerequisites
In order to run the program, you need to install all the requirements listed in [requirements.txt](requirements.txt) using pip


```bash
pip install -r requirements.txt
```
The project has been written using python 3.9 but should work with python 3.6+
## Installation

There are two different launching files.
- [main.py](app/main.py): This file runs a development server with a debug mode that automatically reloads the webpage when the code is updated
```bash
python main.py
```
- [waitressServer.py](app/waitressServer.py): This file runs a production server using  Waitress. This script is used in the [Docker](#docker) image 
```bash
python waitressServer.py
```

## Usage
The default port for the development server is the port 8050. You can change this directly in the code if you want to use a different port.

The default port for the waitress server is defined by the **PORT** environment variable.

### Webpage
You can access the webpage by going to the root address of your server. It will automatically be redirected to the **http://[yourServerAddress]/dash** page which contains the webApp 

Once on the webpage, you need to upload a CSV file with the following format:


| employee_ID | distance_in_m | time_in_s | CO2_in_g |
|-------------|---------------|-----------|----------|
| 1           | 2760          | 1692      | 31678    |
| 2           | 1223          | 983       | 8707     |
| 3           | 610           | 562       | 1762     |

In your CSV file, you need at least the last three columns strictly respecting the names. The data contained must be real numbers

### API
The application has an API that can be accessed using the following link **http://[yourServerAddress]/api**

You can use two different parameters:
- **raw**: The value of this parameter is a csv file written in plain text
- **link**: The value of this parameter is a link to a specific CSV file that can be openly accessed


The API will return a plain text in CSV format with two more columns:
- **cat**: This column contains the raw clustering done by the k-means algorithm
- **transport_mean**: This column contains our interpretation of the K-means algorithm and has 3 possible values:
    - car
    - public transport
    - bike
    
You can find an example in the [test_requests.py](test_requests.py) file
    
## Docker

A Docker image of this project has been created in order to facilitate the deployment of the application. It can be found [here](https://hub.docker.com/repository/docker/flobaudry/employee-segmentation)

To start the docker, you need to bind the ports. As said before, the default port of the application is **8080**.

If you have docker installed, you can run:
```bash
docker pull flobaudry/employee-segmentation
docker run -d -p 8050:8080 flobaudry/employee-segmentation
```
after that, you should be able to access the web application using [this address](http://127.0.0.1:8050/dash)
