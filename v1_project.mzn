include "data.dzn";

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
array[1..number_of_vehicles] of int: can_Take;
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

%Actions
%int : number_of_actions;
%array[1..number_of_actions] of var int: actions_patients_IDs;
%array[1..number_of_actions] of var int: depart_time;
%array[1..number_of_actions] of var int: vehicule_associated;
%array[1..number_of_actions] of var int: arrival_time;
%array[1..number_of_actions] of var int: duration;
%array[1..number_of_actions] of var int: actions_start_location;
%array[1..number_of_actions] of var int: actions_end_location;
%array[1..number_of_actions] of var bool: forward_or_backward;

%DistMatrix
array[1..number_of_places, 1..number_of_places] of int : distMatrix;

% Decision variables
var int :number_of_requests;

%Constraints
solve maximize number_of_requests;

