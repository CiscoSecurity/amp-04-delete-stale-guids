from datetime import datetime
from collections import namedtuple
import configparser
import sys
import requests

UTC_NOW = datetime.utcnow()
if len(sys.argv) > 1:
    if str(sys.argv[1] == '-n'):
        noninteractive = True
    else:
        print('Usage: python delete_stale_guids.py <-n>')
        sys.exit()
else:
    noninteractive = False

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

def delete_guid(session, guid, hostname, computers_url):
    '''Delete the supplied GUID
    '''
    url = computers_url + '{}'.format(guid)
    response = session.delete(url)
    response_json = response.json()
    if noninteractive:
        if response.status_code == 200 and response_json['data']['deleted']:
            print('Succesfully deleted: {}'.format(hostname))
        else:
            print('Something went wrong deleting: {}'.format(hostname))
    else:
        now = datetime.now()
        day_string = now.strftime("%Y-%m-%d")
        daytime_string = now.strftime("%Y-%m-%d %H:%M:%S")
        # Log file rotate daily
        with open('log_'+ day_string + '.txt', 'a+', encoding='utf-8') as file_output:
            if response.status_code == 200 and response_json['data']['deleted']:
                file_output.write(daytime_string + ' - Succesfully deleted: {}'.format(hostname) + '\n')
            else:
                file_output.write(daytime_string + ' - Something went wrong deleting: {}'.format(hostname) + '\n')

def get(session, url):
    '''HTTP GET the URL and return the decoded JSON
    '''
    response = session.get(url)
    response_json = response.json()
    return response_json

def main():
    '''The main logic of the script
    '''
    if noninteractive == '-n':
        print('jepp: ', noninteractive)
    else:
        print('nope')
    # Specify the config file
    config_file = 'api.env'

    # Reading the config file to get settings
    config = configparser.RawConfigParser()
    config.read(config_file)
    client_id = config.get('AMPE', 'client_id')
    api_key = config.get('AMPE', 'api_key')
    age_threshold = int(config.get('AMPE', 'age_threshold'))
    cloud = config.get('AMPE', 'cloud')

    # Instantiate requestions session object
    amp_session = requests.session()
    amp_session.auth = (client_id, api_key)

    # Set to store the computer tuples in
    computers_to_delete = set()

    # URL to query AMP
    if cloud == '':
        computers_url = 'https://api.amp.cisco.com/v1/computers/'
    else:
        computers_url = 'https://api.' + cloud + '.amp.cisco.com/v1/computers/'

    # Query the API
    response_json = get(amp_session, computers_url)

    # Print the total number of GUIDs found
    total_guids = response_json['metadata']['results']['total']
    if noninteractive != '-n':
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
        if noninteractive != '-n':
            print('Processing index: {}'.format(index))
        next_batch = process_response_json(response_json, age_threshold)
        computers_to_delete = computers_to_delete.union(next_batch)

    # Output the number of GUIDs found
    if noninteractive != '-n':
        print('Found {} guids that have not been seen for'
              ' at least {} days'.format(len(computers_to_delete), age_threshold))

    if computers_to_delete:
        if noninteractive != '-n':
            print('Writing CSV containing stale GUIDs to stale_guids.csv')
        with open('stale_guids.csv', 'w', encoding='utf-8') as file_output:
            file_output.write('Age in days,GUID,Hostname\n')
            for computer in computers_to_delete:
                file_output.write('{},{},{}\n'.format(computer.age,
                                                      computer.guid,
                                                      computer.hostname))
        # Check if the user wants to GUIDs to be deleted
        if noninteractive != '-n':
            if confirm_delete():
                for computer in computers_to_delete:
                    delete_guid(amp_session, computer.guid, computer.hostname, computers_url)
            else:
                sys.exit('Exiting!')
        else:
            for computer in computers_to_delete:
                    delete_guid(amp_session, computer.guid, computer.hostname, computers_url)

if __name__ == "__main__":
    main()
