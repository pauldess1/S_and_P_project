start_date = [606, 698, 606, 696]
end_date = [611, 703, 611, 701]
executed_status = [1, 1, 1, 1]
vehicle_assigned = [3, 3, 4, 4]
samevehicle_satisfied = [1, 1, 1, 1]
category_satisfied = [1, 1, 1, 1]
horaire_satisfied = [1, 1, 1, 1]
availability_satisfied = [1, 1, 1, 1]
requests_accepted = [1,1]
start_location = [2,0,2,0]
end_location = [0,2,0,2]
activities_patients_IDs = [1,1,2,2]

def accept_matrix(matrix):
    matrix_copy = [x[:] for x in matrix]
    for i in range(len(requests_accepted)):
        if requests_accepted[i] != 1:
            for element in matrix_copy:
                del element[2 * i]
                del element[2 * i]
    return matrix_copy

matrix = [start_date, end_date, vehicle_assigned, start_location, end_location, activities_patients_IDs]
accepted_matrix = accept_matrix(matrix)
sorted_matrix = [list(x) for x in zip(*sorted(zip(*accepted_matrix), key=lambda x: x[2]))]
print(sorted_matrix)

output_format = {
    "requests": sum(requests_accepted),
    "vehicles": []
}

for i in range(len(requests_accepted)):
    if requests_accepted[i]==1:
        tripf = {
        "origin": start_location[2*i],
        "destination": end_location[2*i],
        "arrival": f"{start_date[2*i] // 60}h{start_date[2*i] % 60:02d}",
        "patients": []
        }
        tripb = {
        "origin": start_location[2*i+1],
        "destination": end_location[2*i+1],
        "arrival": f"{start_date[2*i+1] // 60}h{start_date[2*i+1] % 60:02d}",
        "patients": []
        }
        tripb["patients"].append(activities_patients_IDs[2*i+1])
        output_format["vehicles"].append(tripf)
