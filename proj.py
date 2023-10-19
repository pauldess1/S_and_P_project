import json
from minizinc import Solver, Instance, Model
import subprocess
import sys

def elements_not_in_list(L1, L2):
    set_L1 = set(L1)
    set_L2 = set(L2)
    elements_not_in_L2 = list(set_L1 - set_L2)
    return elements_not_in_L2

def duration_in_minutes(duree):
    heures, minutes = map(int, duree.split('h'))
    return heures * 60 + minutes

def interval_in_minutes(time_str):
    time_str_list=[time_str]
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

def search_data_indice(key, key2, max_len_avai,indice):
    first_item = True
    for vehicule in data[key]:
        minizinc_file.write("|")
        firstt_item = True
        for number in vehicule[key2]:
            if not firstt_item:
                minizinc_file.write(", ")
            minizinc_file.write(str((interval_in_minutes(number)[indice])))
            firstt_item = False
        for i in range(max_len_avai-len(vehicule[key2])):
            minizinc_file.write(",")
            minizinc_file.write(str(0)) 
        first_item = False    
    minizinc_file.write("|];\n")

def search_data_canTake(key, key2,max_len):
    first_item = True
    for element in data[key]:
        minizinc_file.write("|")
        firstt_item = True
        for number in element[key2]:
            if not firstt_item:
                minizinc_file.write(", ")
            minizinc_file.write(str(number))
            firstt_item = False
        for i in range(max_len-len(element[key2])):
            minizinc_file.write(",")
            minizinc_file.write(str(-1)) 
        first_item = False

    minizinc_file.write("|") 
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

def write_Globalparameters(data):
    max_len = 0
    for vehicule in data['vehicles']:
        if len(vehicule['canTake'])>max_len:
            max_len = len(vehicule['canTake'])

    max_len_availability = 0
    for vehicule in data['vehicles']:
        if len(vehicule['availability'])>max_len_availability:
            max_len_availability = len(vehicule['availability'])

    minizinc_file.write('%Global parameters \n')
    minizinc_file.write(f"max_wait_duration = {duration_in_minutes(data['maxWaitTime'])};\n")
    minizinc_file.write(f"same_vehicle_backward = {bool_to_int(data['sameVehicleBackward'])};\n")
    minizinc_file.write(f"number_of_places = {len(data['places'])};\n")
    minizinc_file.write(f"number_of_patients = {len(data['patients'])};\n")
    minizinc_file.write(f"number_of_vehicles = {len(data['vehicles'])};\n")
    minizinc_file.write(f"max_len = {max_len};\n")
    minizinc_file.write(f"max_len_availability = {max_len_availability};\n\n")
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
    search_data_canTake("vehicles","canTake",max_len)
    minizinc_file.write(f"starting_depot = [")
    search_data("vehicles","start")
    minizinc_file.write(f"ending_depot = [")
    search_data("vehicles","end")
    minizinc_file.write(f"capacity = [")
    search_data("vehicles","capacity")
    minizinc_file.write(f"vehicle_availability_start = [")
    search_data_indice("vehicles","availability",max_len_availability,0)
    minizinc_file.write(f"vehicle_availability_end = [")
    search_data_indice("vehicles","availability",max_len_availability,1)
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

def accept_matrix(matrix):
    matrix_copy = [x[:] for x in matrix]
    for i in range(len(requests_accepted)):
        if requests_accepted[i] != 1:
            for element in matrix_copy:
                del element[2*i]
                del element[2*i+1]
        else :
            if forward_or_backward[2*i] == -1:
                for element in matrix_copy:
                    del element[2 * i]
            if forward_or_backward[2*i+1] == -1:
                for element in matrix_copy:
                    del element[2 * i+1]
    return matrix_copy

def create_output (start_date, end_date, vehicle_assigned, start_location, end_location, activities_patients_IDs, forward_or_backward):
    matrix = [start_date, end_date, vehicle_assigned, start_location, end_location, activities_patients_IDs, forward_or_backward]
    accepted_matrix = accept_matrix(matrix)
    sorted_matrix = [list(x) for x in zip(*sorted(zip(*accepted_matrix), key=lambda x: x[2]))]
    
    output_format = {
        "requests": sum(requests_accepted),
        "vehicles": []
    }
    current_vehicle = sorted_matrix[2][0]-1
    first_element = True
    first = True

    for k in range(len(sorted_matrix[0])):
        if sorted_matrix[2][k]==current_vehicle :
            if first_element:
                output_format["vehicles"].append({"id": current_vehicle,"trips": []})
            if sorted_matrix[3][k]!=sorted_matrix[4][k-1]:
                    tripbetween = {
                "origin": sorted_matrix[4][k-1],
                "destination": sorted_matrix[3][k],
                "arrival": f"{(sorted_matrix[1][k - 1] + distMatrix[sorted_matrix[4][k - 1]][sorted_matrix[3][k]]) // 60}h{(sorted_matrix[1][k - 1] + distMatrix[sorted_matrix[4][k - 1]][sorted_matrix[3][k]]) % 60:02d}",
                "patients": []}
                    output_format["vehicles"][-1]["trips"].append(tripbetween)

            trip = {
            "origin": sorted_matrix[3][k],
            "destination": sorted_matrix[4][k],
            "arrival": f"{sorted_matrix[1][k] // 60}h{sorted_matrix[1][k] % 60:02d}",
            "patients": [activities_patients_IDs[k]]
            }
            output_format["vehicles"][-1]["trips"].append(trip)
            first_element = False
        else :
            if not first and sorted_matrix[4][k-1]!=ending_depot[current_vehicle-vehicle_IDs[0]]:
                tripe = {
                "origin": sorted_matrix[4][k-1] ,
                "destination": ending_depot[current_vehicle-vehicle_IDs[0]],
                "arrival": f"{(sorted_matrix[1][k - 1] + distMatrix[sorted_matrix[4][k - 1]][ending_depot[current_vehicle - vehicle_IDs[0]]]) // 60}h{(sorted_matrix[1][k - 1] + distMatrix[sorted_matrix[4][k - 1]][ending_depot[current_vehicle - vehicle_IDs[0]]]) % 60:02d}",
                "patients": []
                }
                output_format["vehicles"][-1]["trips"].append(tripe)
            else :
                first = False
            while sorted_matrix[2][k]!=current_vehicle :
                current_vehicle+=1
            output_format["vehicles"].append({"id": current_vehicle,"trips": []})
            tripb = {
            "origin": starting_depot[current_vehicle-vehicle_IDs[0]],
            "destination": sorted_matrix[3][k],
            "arrival": f"{(sorted_matrix[0][k]-srv_duration[activities_patients_IDs[k]-patients_IDs[0]]) // 60}h{(sorted_matrix[0][k]-srv_duration[activities_patients_IDs[k]-patients_IDs[0]]) % 60:02d}",
            "patients": []
            }
            output_format["vehicles"][-1]["trips"].append(tripb)
            trip = {
                "origin": sorted_matrix[3][k],
                "destination": sorted_matrix[4][k],
                "arrival": f"{sorted_matrix[1][k] // 60}h{sorted_matrix[1][k] % 60:02d}",
                "patients": [activities_patients_IDs[k]]
                }
            output_format["vehicles"][-1]["trips"].append(trip)
            first_element = False
    if sorted_matrix[4][-1]!=ending_depot[current_vehicle-vehicle_IDs[0]]:
        tripe = {
                "origin": sorted_matrix[4][-1] ,
                "destination": ending_depot[current_vehicle-vehicle_IDs[0]],
                "arrival": f"{(max(srv_duration)+sorted_matrix[1][- 1] + distMatrix[sorted_matrix[4][- 1]][ending_depot[current_vehicle - vehicle_IDs[0]]]) // 60}h{(max(srv_duration)+sorted_matrix[1][-1] + distMatrix[sorted_matrix[4][-1]][ending_depot[current_vehicle - vehicle_IDs[0]]]) % 60:02d}",
                "patients": []
                }       
        output_format["vehicles"][-1]["trips"].append(tripe)
    all_vehicles = vehicle_IDs
    vehicles_with_trips = list(set(vehicle_assigned))
    vehicles_without_trips = elements_not_in_list(all_vehicles, vehicles_with_trips)
    for vehicle_id in vehicles_without_trips:
        output_format["vehicles"].append({"id": vehicle_id, "trips": []})

    return output_format



if len(sys.argv) != 3:
    print("Usage: python proj.py <input-file-name> <output-file-name>")
else:
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    try:
        # Read input JSON data from the specified file
        with open(input_file_name, 'r') as json_file:
            data = json.load(json_file)

        # Generate MiniZinc code and write it to 'data.dzn' file
        with open(r'data.dzn', 'w') as minizinc_file:
            write_Globalparameters(data)

        # Execute MiniZinc model and process the output
        minizinc_output = subprocess.check_output(["minizinc", "v1_project.mzn"]).decode("utf-8")
        start_index = minizinc_output.find('{')
        end_index = minizinc_output.rfind('}') + 1
        json_output = minizinc_output[start_index:end_index]
        result = json.loads(json_output)

        # Extract relevant data from the MiniZinc output
        executed_status = result['executed_status']
        forward_or_backward = result['forward_or_backward']
        start_date = result['start_date']
        end_date = result['end_date']
        vehicle_assigned = result['vehicle_assigned']
        requests_accepted = result['requests_accepted']
        start_location = result['start_location']
        end_location = result['end_location']
        activities_patients_IDs = result['activities_patients_IDs']
        distMatrix = data['distMatrix']
        starting_depot = result['starting_depot']
        ending_depot = result['ending_depot']
        vehicle_IDs = result['vehicle_IDs']
        srv_duration = result['srv_duration']
        patients_IDs = result['patients_IDs']
        vehicle_IDs = result['vehicle_IDs']

        # Create the output data structure
        output_data = create_output(start_date, end_date, vehicle_assigned, start_location, end_location,
                                    activities_patients_IDs, forward_or_backward)

        # Write the output data to the specified output file
        with open(output_file_name, 'w') as output_file:
            json.dump(output_data, output_file)

    except FileNotFoundError:
        print("Error: The specified input file was not found.")
    except json.JSONDecodeError:
        print("Error: The input file is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

