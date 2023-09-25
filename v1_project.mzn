% Use this editor as a MiniZinc scratch book
int: max_wait_duration;
bool: same_vehicle_backward;

%Vehicules
int : number_of_vehicules;
array[1..number_of_vehicules] of int: vehicle_IDs;
array[1..number_of_vehicules] of int: vehicle_capacity;
array[1..number_of_vehicules] of int: vehicle_category;
array[1..number_of_vehicules] of int: vehicle_availability; %array of array !!
array[1..number_of_vehicules] of int: starting_depot;
array[1..number_of_vehicules] of int: ending_depot;

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
int : number_of_actions;
array[1..number_of_actions] of int: actions_patients_IDs;
array[1..number_of_actions] of int: depart_time;
array[1..number_of_actions] of int: vehicule_associated;
array[1..number_of_actions] of int: arrival_time;
array[1..number_of_actions] of int: duration;
array[1..number_of_actions] of int: actions_start_location;
array[1..number_of_actions] of int: actions_end_location;
array[1..number_of_actions] of bool: forward_or_backward;

%Distance Matrix
int : number_of_locations;
set of int: HEIGHT = 0..number_of_locations;
set of int: WIDTH = 0..number_of_locations;
array[HEIGHT,WIDTH] of var int: Dist_Matrix;

% Decision variables
int :number_of_requests;
array[1..number_of_requests] of 0..1: accepted_request;



% Contraintes
% Les actions attribuées au même véhicule ne doivent pas se chevaucher dans le temps
constraint forall(v in 1..number_of_vehicules)(
    forall(a1, a2 in 1..number_of_actions where a1 < a2)(
        (assigned_vehicle[a1] == v /\ assigned_vehicle[a2] == v) ->
        ()
    )

