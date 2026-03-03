import LAMP
import csv
import datetime
from decouple import config
from utility import ensure_parent_dir, get_num_input_from_list

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


# Export activity data for each participant
result = {}
for identifier in participants_to_export:
    print(f"Fetching data for participant: {identifier}")
    activity_data = LAMP.ActivityEvent.all_by_participant(identifier)['data']
    result[identifier] = activity_data
    print(f"Fetched {len(activity_data)} events for participant {identifier}")

# Define CSV file name
csv_filename = f'output/activity/aexport_activity_{name}_{str(datetime.datetime.now()).split(" ")[0]}.csv'
ensure_parent_dir(csv_filename)  # Ensure the parent directory exists before writing to the file

# Write to CSV
try:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['participant_id', 'timestamp', 'activity', 'duration', 'item', 'value', 'type', 'level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for participant_id, events in result.items():
            for event in events:
                for slice in event['temporal_slices']:
                    writer.writerow({
                        'participant_id': participant_id,
                        'timestamp': event.get('timestamp'),
                        'activity': event.get('activity'),
                        'duration': event.get('duration'),
                        'item': slice.get('item'),
                        'value': slice.get('value'),
                        'type': slice.get('type'),
                        'level': slice.get('level')
                    })
    print(f"CSV file '{csv_filename}' created successfully.")
except Exception as e:
    print(f"Error writing to CSV file: {e}")

