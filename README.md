### AMP for Endpoints SHA256 to command line arguments

Script will query an AMP for Endpoints environment and collect all GUIDs that have not been seen for 60 days or more. It will write them to disk in a CSV with the Age in days, GUID, and Hostname. The user will be prompted if they would like to delete the stale GUIDs. If they answer y the script will delete stale GUIDs from the environment

### Before using you must update the following:
The authentictaion parameters are set in the ```api.cfg``` :
- client_id 
- api_key

### Usage
```
python delete_stale_guids.py
```

### Example script output:  
```
Found 33 guids that have not been seen for at least 60 days
Writing CSV containing stale GUIDs to stale_guids.csv
Do you want to delete inactive GUIDs? (y/n): y
Succesfully deleted: Demo_AMP_Exploit_Prevention_Audit
Succesfully deleted: Demo_Qakbot_1
Succesfully deleted: Demo_Stabuniq
Succesfully deleted: Demo_Qakbot_2
Succesfully deleted: Demo_AMP_Threat_Quarantined
Succesfully deleted: Demo_Dyre
Succesfully deleted: Demo_Command_Line_Arguments_Kovter
Succesfully deleted: Demo_iOS_3
Succesfully deleted: Demo_AMP_Intel
Succesfully deleted: Demo_AMP
Succesfully deleted: Demo_Dridex
Succesfully deleted: Demo_CryptoWall
Succesfully deleted: Demo_TeslaCrypt
Succesfully deleted: Demo_Ramnit
Succesfully deleted: Demo_Cta
Succesfully deleted: Demo_Plugx
Succesfully deleted: Demo_iOS_1
Succesfully deleted: Demo_WannaCry_Ransomware
Succesfully deleted: Demo_CozyDuke
Succesfully deleted: Demo_Low_Prev_Retro
Succesfully deleted: Demo_AMP_Exploit_Prevention
Succesfully deleted: Demo_Tinba
Succesfully deleted: Demo_iOS_4
Succesfully deleted: Demo_Qakbot_3
Succesfully deleted: Demo_TDSS
Succesfully deleted: Demo_Zbot
Succesfully deleted: Demo_AMP_Threat_Audit
Succesfully deleted: Demo_Command_Line_Arguments_Meterpreter
Succesfully deleted: Demo_iOS_2
Succesfully deleted: Demo_ZAccess
Succesfully deleted: Demo_Upatre
Succesfully deleted: Demo_iOS_5
Succesfully deleted: Demo_SFEicar
```
