v2 - Procom Santé Connectée - updated 2/2026

v1 - Initial codebase and README by Mr. Punn Chunwimaleung (2024)

# Export Activity and Sensor Data Script

This script exports activity & sensor data from the mindLAMP platform for selected participants within a researcher's study.

## Prerequisites

- Python 3.7 or higher
- `pip` package manager

## Setup Instructions

### 1. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps to manage dependencies and avoid conflicts with other projects.

`python -m venv lamp_env`

and activate it:

On Mac and Linux use `source lamp_env/bin/activate` <br>
On Windows use `lamp_env\bin\activate`


### 2. Install Required Packages
Make sure you have pip installed. Then, install the necessary packages:

`pip install -r requirements.txt`

### 3. Create a `.env` File

Create a `.env` file in the root directory of the project and add the following variables (see example `sample.env`):

```
URL=<your_lamp_server_url>
EMAIL=<your_lamp_email>
PASSWORD=<your_lamp_password>
RESEARCHER=<your_researcher_id>
```

To get the `RESEARCHER` ID:
1. Log in to the mindLAMP platform.
2. Click on the `Data Portal` tab.
3. Copy the Researcher ID:
![alt text](researcher_id.png)

### 4. Run the Script

Run the script with the following command:

for exporting activity data:
`python export_data_activity.py`

or

for exporting sensor data:
`python export_sensor_data_sensor_csv.py`

or

for both export process
`python export_both.py`



