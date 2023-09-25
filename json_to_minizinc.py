import json

def duration_in_minutes(duree):
    heures, minutes = map(int, duree.split('h'))
    return heures * 60 + minutes

def interval_in_minutes(time_str_list):
    result = []
    for time_str in time_str_list:
        parts = time_str.split(':')
        result.append([duration_in_minutes(parts[0]), duration_in_minutes(parts[1])])
    return result[0]

def bool_to_int(valeur_bool):
    return int(valeur_bool) 

def search_data(key, key2):
    first_item = True
    for element in data[key]:
        if not first_item:
            minizinc_file.write(", ")
        minizinc_file.write(str(element[key2]))
        first_item = False
    minizinc_file.write("];\n")

def search_data_time(key, key2):
    first_item = True
    for element in data[key]:
        if not first_item:
            minizinc_file.write(", ")
        minizinc_file.write(str(duration_in_minutes(element[key2])))
        first_item = False
    minizinc_file.write("];\n")

def search_data_interval(key, key2):
    first_item = True
    for element in data[key]:
        if not first_item:
            minizinc_file.write(", ")
        minizinc_file.write(str(interval_in_minutes(element[key2])))
        first_item = False
    minizinc_file.write("];\n")
    
# Load JSON data
with open(r'C:\Users\pauld\Desktop\TECNICO\Search and Planning\Project\instances\easy\easy_1.json', 'r') as json_file:
    data = json.load(json_file)

# Open MiniZinc file for writing
with open(r'C:\Users\pauld\Desktop\TECNICO\Search and Planning\Project\test_python.mzn', 'w') as minizinc_file:

    #Global parameters
    minizinc_file.write('%Global parameters \n')
    minizinc_file.write(f"int: max_wait_duration = {duration_in_minutes(data['maxWaitTime'])};\n")
    minizinc_file.write(f"bool: same_vehicle_backward = {bool_to_int(data['sameVehicleBackward'])};\n")
    minizinc_file.write(f"int: number_of_places = {len(data['places'])};\n")
    minizinc_file.write(f"int: number_of_patients = {len(data['patients'])};\n")
    minizinc_file.write(f"int: number_of_vehicles = {len(data['vehicles'])};\n\n")


    #Places
    minizinc_file.write('%Places \n')
    minizinc_file.write(f"array[1..number_of_places] of int: places_ID = [")
    search_data("places","id")
    minizinc_file.write(f"array[1..number_of_places] of int: places_category = [")
    search_data("places","category")
    minizinc_file.write("\n")

    #Vehicules 
    minizinc_file.write('%Vehicles \n')
    minizinc_file.write(f"array[1..number_of_vehicles] of int: vehicle_IDs = [")
    search_data("vehicles","id")
    minizinc_file.write(f"array[1..number_of_vehicles] of int: can_Take = [")
    search_data("vehicles","canTake")
    minizinc_file.write(f"array[1..number_of_vehicles] of int: starting_depot = [")
    search_data("vehicles","start")
    minizinc_file.write(f"array[1..number_of_vehicles] of int: ending_depot = [")
    search_data("vehicles","end")
    minizinc_file.write(f"array[1..number_of_vehicles] of int: capacity = [")
    search_data("vehicles","capacity")
    minizinc_file.write(f"array[1..number_of_vehicles] of int: availability = [")
    search_data_interval("vehicles","availability")

    #Patients
    minizinc_file.write('% Patients \n')
    minizinc_file.write('array[1..number_of_patients] of int: patients_IDs = [')
    search_data("patients", "id")
    minizinc_file.write('array[1..number_of_patients] of int: patients_load = [')
    search_data("patients", "load")
    minizinc_file.write('array[1..number_of_patients] of int: patients_category = [')
    search_data("patients", "category")
    minizinc_file.write('array[1..number_of_patients] of int: patients_start_location = [')
    search_data("patients", "start")
    minizinc_file.write('array[1..number_of_patients] of int: patients_destination = [')
    search_data("patients", "destination")
    minizinc_file.write('array[1..number_of_patients] of int: patients_end_location = [')
    search_data("patients", "end")
    minizinc_file.write('array[1..number_of_patients] of int: rdv_time = [')
    search_data_time("patients", "rdvTime")
    minizinc_file.write('array[1..number_of_patients] of int: rdv_duration = [')
    search_data_time("patients", "rdvDuration")
    minizinc_file.write('array[1..number_of_patients] of int: srv_duration = [')
    search_data_time("patients", "srvDuration")


    



minizinc_file.close()

print("MiniZinc code generated successfully.")
