include "data.dzn";
include "cumulative.mzn";

% Use this editor as a MiniZinc scratch book
int: max_wait_duration;
int: same_vehicle_backward;
int: number_of_places;

%Places
array[1..number_of_places] of int: places_ID;
array[1..number_of_places] of int: places_category;


%Vehicules
int : number_of_vehicles;
array[1..number_of_vehicles] of int: vehicle_IDs;
array[1..number_of_vehicles] of int: capacity;
array[1..number_of_vehicles] of int: can_Take; %could have several values, array of array
array[1..number_of_vehicles] of int: vehicle_availability_start;
array[1..number_of_vehicles] of int: vehicle_availability_end;
array[1..number_of_vehicles] of int: starting_depot;
array[1..number_of_vehicles] of int: ending_depot;

%Patients
int : number_of_patients;
array[1..number_of_patients] of int: patients_IDs;
array[1..number_of_patients] of int: patients_load;
array[1..number_of_patients] of int: patients_category;
array[1..number_of_patients] of int: patients_start_location;
array[1..number_of_patients] of int: patients_destination;
array[1..number_of_patients] of int: patients_end_location;
array[1..number_of_patients] of int: rdv_time;
array[1..number_of_patients] of int: rdv_duration;
array[1..number_of_patients] of int: srv_duration;

%Activities
int : number_of_activities;
array[1..number_of_activities] of int: activities_patients_IDs;
array[1..number_of_activities] of var int: start_date;
array[1..number_of_activities] of var int: end_date;
array[1..number_of_activities] of var int: start_location;
array[1..number_of_activities] of var int: end_location;
array[1..number_of_activities] of int: duration_of_trip;
array[1..number_of_activities] of int: forward_or_backward;
array[1..number_of_activities] of var 0..1: executed_status;
array[1..number_of_activities] of var int: vehicle_assigned;
array[1..number_of_activities] of var int: activities_load;




array[1..number_of_patients] of int: requests_accepted = array1d(1..number_of_patients, [0 | i in 1..number_of_patients]);



%DistMatrix
array[1..number_of_places, 1..number_of_places] of int : distMatrix;

%Constraints
constraint forall(i in 1..number_of_activities) (
    if forward_or_backward[i] = 1 then
        rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] - srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] > end_date[i] /\  %we don't need to put the 0 because it will be solved by the vehicle availibility
        rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] - srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] - max_wait_duration < end_date[i] /\ duration_of_trip[i] = end_date[i]-start_date[i]  
    else
        rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] + rdv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] + srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] < start_date[i] /\
        rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] + rdv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] + srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] + max_wait_duration > start_date[i] /\ duration_of_trip[i] = end_date[i]-start_date[i]       
    endif
);

constraint forall(i in 1..number_of_activities) (
  can_Take[vehicle_assigned[i] - vehicle_IDs[1] + 1] = patients_category[activities_patients_IDs[i] - patients_IDs[1] + 1]);

constraint forall(i in 1..number_of_activities, j in 1..number_of_activities)(
  if (vehicle_assigned[i] == vehicle_assigned[j]) /\ (i != j) then 
  start_date[j]-start_date[i] >= distMatrix[start_location[i],start_location[j]]+ srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] \/ start_date[i]-start_date[j] >= distMatrix[start_location[j],start_location[i]]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1]
  /\
  start_date[j]-end_date[i] >= distMatrix[end_location[i],start_location[j]] \/ end_date[i]-start_date[j] >= distMatrix[start_location[j],end_location[i]]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1]+srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]
  /\
  end_date[j]-start_date[i] >= distMatrix[start_location[i],end_location[j]]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1]+srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] \/ start_date[i]-end_date[j] >= distMatrix[end_location[j],start_location[i]]
  /\
  end_date[j]-end_date[i] >= distMatrix[end_location[i],end_location[j]]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1] \/ end_date[i]-end_date[j] >= distMatrix[end_location[j],end_location[i]]+ srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]
  endif);
  

constraint forall(i in 0..number_of_patients)(
    if executed_status[i*2+1] == 1 /\ executed_status[(i+1)*2] == 1 
    then 
        requests_accepted[i+1] = 1
    endif
);

constraint forall(v in 1..number_of_vehicles)(
  cumulative(start_date, duration_of_trip, activities_load, capacity[v])
  );
  
solve maximize sum(requests_accepted);
%output [show(executed_status)]

