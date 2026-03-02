import LAMP
import csv
import datetime
from decouple import config
from utility import get_num_input_from_list
import json
from zoneinfo import ZoneInfo
import os

# Connect to LAMP server
LAMP.connect(server_address=config('URL', cast=str),
             access_key=config('EMAIL', cast=str),
             secret_key=config('PASSWORD', cast=str))


# Retrieve study with name "Procom"
studies_by_researcher = LAMP.Study.all_by_researcher(config('RESEARCHER', cast=str))
studies_by_researcher = studies_by_researcher['data']
study = next((s for s in studies_by_researcher if s["name"] == "Procom"), None)
if not study:
    raise ValueError("Study 'Procom' not found.")

print(f"Selected study: {study['name']}")

# Retrieve all participants by study
participants = LAMP.Participant.all_by_study(study['id'])['data']
print(f"Found {len(participants)} participants in study 'Procom'.")

# select all participants
participants_to_export = [participant['id'] for participant in participants]
name = 'all'
print(f"Selected all participants for export.")

# Fetch sensor data for each participant
result = {}
for identifier in participants_to_export:
    result[identifier] = LAMP.SensorEvent.all_by_participant(identifier)['data']
    print(f"Fetched {len(result[identifier])} sensor events for participant {identifier}.")  

#print total number of sensor events fetched
total_events = sum(len(events) for events in result.values())
print(f"Total sensor events fetched for all participants: {total_events}")

#filter by sensor type "lamp.*"
for participant_id, events in result.items():
    filtered_events = [event for event in events if event['sensor'].startswith('lamp.')]
    result[participant_id] = filtered_events
    print(f"After filtering, {len(filtered_events)} 'lamp.*' sensor events remain for participant {participant_id}.")


# Define CSV file name
csv_filename = f'output/sensor/general/general_lamp_export_sensor_{name}_{str(datetime.datetime.now()).split(" ")[0]}.csv'

# Write to CSV - general export
try:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['participant_id', 'timestamp', 'sensor', 'data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for participant_id, events in result.items():
            for event in events:
                writer.writerow({
                    'participant_id': participant_id,
                    'timestamp': datetime.datetime.fromtimestamp(event['timestamp'] / 1000, tz=ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S"),
                    'sensor': event['sensor'],
                    'data': json.dumps(event['data'])
                })
    print(f"Data successfully exported to {csv_filename}")
except Exception as e:
    print(f"An error occurred while writing to CSV: {e}")



# explode each event's `data` field so every key in the data dict becomes its own CSV column
sensor_types = set()
for events in result.values():
    for event in events:
        sensor_types.add(event['sensor'])
for sensor_type in sensor_types:
    csv_filename = f'output/sensor/{sensor_type}_export_sensor_{name}_{str(datetime.datetime.now()).split(" ")[0]}.csv'
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # determine all possible keys in data field for this sensor type
            data_keys = set()
            for participant_id, events in result.items():
                for event in events:
                    if event['sensor'] == sensor_type:
                        data_keys.update(event['data'].keys())

            # defining fieldnames for CSV
            fieldnames = ['participant_id', 'date', 'time', 'sensor'] + list(data_keys)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # write header and rows
            tz = ZoneInfo("Europe/Paris")
            writer.writeheader()
            for participant_id, events in result.items():
                for event in events:
                    if event['sensor'] == sensor_type:
                        ts = event.get("timestamp")

                        # just in case timestamp is missing, skip this event
                        if ts is None:
                            continue
                        
                        # convert timestamp to datetime with timezone
                        dt = datetime.datetime.fromtimestamp(float(ts) / 1000.0, tz=tz)
                        
                        row = {
                            'participant_id': participant_id,
                            #'timestamp': datetime.datetime.fromtimestamp(event['timestamp'] / 1000, tz=ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S"),
                            "date": dt.strftime("%Y-%m-%d"),
                            "time": dt.strftime("%H:%M:%S"),
                            'sensor': event['sensor']
                        }
                        row.update(event['data'])
                        writer.writerow(row)
        print(f"Data for sensor {sensor_type} successfully exported to {csv_filename}")
    except Exception as e:
        print(f"An error occurred while writing data for sensor {sensor_type} to CSV: {e}")

