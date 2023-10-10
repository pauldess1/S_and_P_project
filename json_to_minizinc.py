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

def search_data_indice(key, key2, indice):
    first_item = True
    for element in data[key]:
        if not first_item:
            minizinc_file.write(", ")
        minizinc_file.write(str((interval_in_minutes(element[key2])[indice])))
        first_item = False
    minizinc_file.write("];\n")

def search_data_canTake(key, key2):
    first_item = True
    for element in data[key]:
        if not first_item:
            minizinc_file.write(", ")
        minizinc_file.write(str(element[key2][0]))
        first_item = False
    minizinc_file.write("];\n")

def matrix(matrix):
    minizinc_file.write("[")
    first_line = True
    for i in range(len(matrix)):
        if first_line:
            minizinc_file.write("| ")
        first_line=False
        first_item = True
        for j in range(len(matrix[0])):
            if not first_item:
                minizinc_file.write(", ")
            minizinc_file.write(str(matrix[i][j]))
            first_item = False
        minizinc_file.write("|")
    minizinc_file.write("];")

def activities_creation():
    activities_patients_IDs = []
    duration_of_trip = []
    forward_or_backward=[]
    start_location=[]
    end_location=[]
    for json in data["patients"]:
        if json['start']== (-1):
            forward_or_backward.append(-1)
        else : 
            forward_or_backward.append(1)

        activities_patients_IDs.append(json["id"])
        duration_of_trip.append(data['distMatrix'][json['start']][json['destination']])
        start_location.append(json['start'])
        end_location.append(json['destination'])
        activities_patients_IDs.append(json["id"])
        if json['end']== (-1):
            forward_or_backward.append(-1)
        else : 
            forward_or_backward.append(0)
        duration_of_trip.append(data['distMatrix'][json['end']][json['destination']])
        start_location.append(json['destination'])
        end_location.append(json['end'])

    minizinc_file.write("activities_patients_IDs = [")
    first_element = True
    for i in range(len(activities_patients_IDs)):
        if not first_element:
            minizinc_file.write(",")
        first_element=False
        minizinc_file.write(str(activities_patients_IDs[i]))
    minizinc_file.write("];\n")
    minizinc_file.write("duration_of_trip = [")
    first_element = True
    for i in range(len(duration_of_trip)):
        if not first_element:
            minizinc_file.write(",")
        first_element=False
        minizinc_file.write(str(duration_of_trip[i]))
    minizinc_file.write("];\n")

    minizinc_file.write("forward_or_backward = [ ")
    first_element = True
    for i in range(len(forward_or_backward)):
        if not first_element:
            minizinc_file.write(",")
        first_element=False
        minizinc_file.write(str(forward_or_backward[i]))
    minizinc_file.write("];\n")
    minizinc_file.write('number_of_activities = ' + str(len(forward_or_backward)) + ';\n')

    minizinc_file.write("start_location = [ ")
    first_element = True
    for i in range(len(forward_or_backward)):
        if not first_element:
            minizinc_file.write(",")
        first_element=False
        minizinc_file.write(str(start_location[i]))
    minizinc_file.write("];\n")

    minizinc_file.write("end_location = [ ")
    first_element = True
    for i in range(len(forward_or_backward)):
        if not first_element:
            minizinc_file.write(",")
        first_element=False
        minizinc_file.write(str(end_location[i]))
    minizinc_file.write("];\n")


    
# Load JSON data
with open(r'C:\Users\pauld\Desktop\TECNICO\Search and Planning\Project\custom\custom_1.json', 'r') as json_file:
    data = json.load(json_file)

# Open MiniZinc file for writing
with open(r'C:\Users\pauld\Desktop\TECNICO\Search and Planning\Project\data.dzn', 'w') as minizinc_file:

    #Global parameters
    minizinc_file.write('%Global parameters \n')
    minizinc_file.write(f"max_wait_duration = {duration_in_minutes(data['maxWaitTime'])};\n")
    minizinc_file.write(f"same_vehicle_backward = {bool_to_int(data['sameVehicleBackward'])};\n")
    minizinc_file.write(f"number_of_places = {len(data['places'])};\n")
    minizinc_file.write(f"number_of_patients = {len(data['patients'])};\n")
    minizinc_file.write(f"number_of_vehicles = {len(data['vehicles'])};\n\n")


    #Places
    minizinc_file.write('%Places \n')
    minizinc_file.write(f"places_ID = [")
    search_data("places","id")
    minizinc_file.write(f"places_category = [")
    search_data("places","category")
    minizinc_file.write("\n")

    #Vehicules 
    minizinc_file.write('%Vehicles \n')
    minizinc_file.write(f"vehicle_IDs = [")
    search_data("vehicles","id")
    minizinc_file.write(f"can_Take = [")
    search_data_canTake("vehicles","canTake")
    minizinc_file.write(f"starting_depot = [")
    search_data("vehicles","start")
    minizinc_file.write(f"ending_depot = [")
    search_data("vehicles","end")
    minizinc_file.write(f"capacity = [")
    search_data("vehicles","capacity")
    minizinc_file.write(f"vehicle_availability_start = [")
    search_data_indice("vehicles","availability",0)
    minizinc_file.write(f"vehicle_availability_end = [")
    search_data_indice("vehicles","availability",1)

    #Patients
    minizinc_file.write('% Patients \n')
    minizinc_file.write('patients_IDs = [')
    search_data("patients", "id")
    minizinc_file.write('patients_load = [')
    search_data("patients", "load")
    minizinc_file.write('patients_category = [')
    search_data("patients", "category")
    minizinc_file.write('patients_start_location = [')
    search_data("patients", "start")
    minizinc_file.write('patients_destination = [')
    search_data("patients", "destination")
    minizinc_file.write('patients_end_location = [')
    search_data("patients", "end")
    minizinc_file.write('rdv_time = [')
    search_data_time("patients", "rdvTime")
    minizinc_file.write('rdv_duration = [')
    search_data_time("patients", "rdvDuration")
    minizinc_file.write('srv_duration = [')
    search_data_time("patients", "srvDuration")

    #Activities
    minizinc_file.write('% Activities \n')
    activities_creation()
    


    #Dist Matrix
    minizinc_file.write(f"distMatrix = ")
    matrix(data['distMatrix'])

minizinc_file.close()

print("MiniZinc code generated successfully.")
