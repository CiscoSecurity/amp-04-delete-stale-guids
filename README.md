[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/AMP-for-Endpoints "Gitter chat")

### AMP for Endpoints Delete Stale GUIDs:

Script will query an AMP for Endpoints environment and collect all GUIDs that have not been seen for 60 days or more. It will write them to disk in a CSV with the Age in days, GUID, and Hostname. The user will be prompted if they would like to delete the stale GUIDs. If they answer y the script will delete stale GUIDs from the environment.

For large environments (50k+ GUIDs) this script may take over 30 minutes to complete.

### Before using you must update ```api.cfg```:
Authentication parameters:
- client_id 
- api_key
Delete all GUIDs older than this value:
- age_treshold
Choose cloud location. Set to eu for European Union, apjc for Asia Pacific, Japan, and Greater China or leave empty for North America:
- cloud

### Usage:
```
python delete_stale_guids.py
```

### Example script output:  
```
GUIDs found in environment: 471
Found 33 guids that have not been seen for at least 60 days
Writing CSV containing stale GUIDs to stale_guids.csv
Do you want to delete inactive GUIDs? (y/n): y
Succesfully deleted: Demo_Dyre
Succesfully deleted: Demo_iOS_4
Succesfully deleted: Demo_SFEicar
Succesfully deleted: Demo_Low_Prev_Retro
Succesfully deleted: Demo_Zbot
Succesfully deleted: Demo_Ramnit
Succesfully deleted: Demo_iOS_2
Succesfully deleted: Demo_Qakbot_1
Succesfully deleted: Demo_WannaCry_Ransomware
Succesfully deleted: Demo_Dridex
Succesfully deleted: Demo_Qakbot_3
Succesfully deleted: Demo_Stabuniq
Succesfully deleted: Demo_AMP_Exploit_Prevention_Audit
Succesfully deleted: Demo_Command_Line_Arguments_Meterpreter
Succesfully deleted: Demo_AMP_Exploit_Prevention
Succesfully deleted: Demo_Upatre
Succesfully deleted: Demo_iOS_5
Succesfully deleted: Demo_Tinba
Succesfully deleted: Demo_ZAccess
Succesfully deleted: Demo_Plugx
Succesfully deleted: Demo_AMP_Threat_Audit
Succesfully deleted: Demo_Qakbot_2
Succesfully deleted: Demo_TDSS
Succesfully deleted: Demo_TeslaCrypt
Succesfully deleted: Demo_AMP_Intel
Succesfully deleted: Demo_CryptoWall
Succesfully deleted: Demo_AMP
Succesfully deleted: Demo_iOS_3
Succesfully deleted: Demo_Cta
Succesfully deleted: Demo_CozyDuke
Succesfully deleted: Demo_iOS_1
Succesfully deleted: Demo_AMP_Threat_Quarantined
Succesfully deleted: Demo_Command_Line_Arguments_Kovter
```
