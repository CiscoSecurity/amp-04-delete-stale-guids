from datetime import datetime
from collections import namedtuple
import configparser
import sys
import requests

UTC_NOW = datetime.utcnow()

def calculate_time_delta(timestamp):
    '''Calculate how long it has been since the GUID was last seen
    '''
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_object = datetime.strptime(timestamp, time_format)
    age = (UTC_NOW - datetime_object).days
    return age

def should_delete(age, threshold):
    '''Check if the GUID age is greater than the configured threshold
    '''
    if age > threshold:
        return True
    return False

def process_guid_json(guid_json):
    '''Process the individual GUID entry
    '''
    computer = namedtuple('computer', ['hostname', 'guid', 'age'])
    connector_guid = guid_json.get('connector_guid')
    hostname = guid_json.get('hostname')
    last_seen = guid_json.get('last_seen')
    age = calculate_time_delta(last_seen)
    return computer(hostname, connector_guid, age)

def process_response_json(json, age_threshold):
    '''Process the decoded JSON blob from /computers
    '''
    computers_to_delete = set()
    for entry in json['data']:
        computer = process_guid_json(entry)
        if should_delete(computer.age, age_threshold):
            computers_to_delete.add(computer)
    return computers_to_delete

def confirm_delete():
    '''Ask the user if they want to delete the GUIDs
    '''
    while True:
        reply = str(input('Do you want to delete inactive GUIDs?'+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

def delete_guid(session, guid, hostname):
    '''Delete the supplied GUID
    '''
    url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
    response = session.delete(url)
    response_json = response.json()

    if response.status_code == 200 and response_json['data']['deleted']:
        print('Succesfully deleted: {}'.format(hostname))
    else:
        print('Something went wrong deleting: {}'.format(hostname))

def get(session, url):
    '''HTTP GET the URL and return the decoded JSON
    '''
    response = session.get(url)
    response_json = response.json()
    return response_json

def main():
    '''The main logic of the script
    '''

    # Specify the config file
    config_file = 'api.cfg'

    # Reading the config file to get settings
    config = configparser.RawConfigParser()
    config.read(config_file)
    client_id = config.get('AMPE', 'client_id')
    api_key = config.get('AMPE', 'api_key')
    age_threshold = int(config.get('AMPE', 'age_threshold'))

    # Instantiate requestions session object
    amp_session = requests.session()
    amp_session.auth = (client_id, api_key)

    # Set to store the computer tuples in
    computers_to_delete = set()

    # URL to query AMP
    computers_url = 'https://api.amp.cisco.com/v1/computers'

    # Query the API
    response_json = get(amp_session, computers_url)

    # Print the total number of GUIDs found
    total_guids = response_json['metadata']['results']['total']
    print('GUIDs found in environment: {}'.format(total_guids))

    # Process the returned JSON
    initial_batch = process_response_json(response_json, age_threshold)

    # Store the returned stale GUIDs
    computers_to_delete = computers_to_delete.union(initial_batch)

    # Check if there are more pages and repeat
    while 'next' in response_json['metadata']['links']:
        next_url = response_json['metadata']['links']['next']
        response_json = get(amp_session, next_url)
        index = response_json['metadata']['results']['index']
        print('Processing index: {}'.format(index))
        next_batch = process_response_json(response_json, age_threshold)
        computers_to_delete = computers_to_delete.union(next_batch)

    # Output the number of GUIDs found
    print('Found {} guids that have not been seen for'
          ' at least {} days'.format(len(computers_to_delete), age_threshold))

    if computers_to_delete:
        print('Writing CSV containing stale GUIDs to stale_guids.csv')
        with open('stale_guids.csv', 'w', encoding='utf-8') as file_output:
            file_output.write('Age in days,GUID,Hostname\n')
            for computer in computers_to_delete:
                file_output.write('{},{},{}\n'.format(computer.age,
                                                      computer.guid,
                                                      computer.hostname))
        # Check if the user wants to GUIDs to be deleted
        if confirm_delete():
            for computer in computers_to_delete:
                delete_guid(amp_session, computer.guid, computer.hostname)
        else:
            sys.exit('Exiting!')

if __name__ == "__main__":
    main()
