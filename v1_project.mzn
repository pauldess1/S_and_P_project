include "data.dzn";
include "cumulative.mzn";

% Use this editor as a MiniZinc scratch book
int: max_wait_duration;
int: same_vehicle_backward;
int: number_of_places;
int : max_len;
int : max_len_availability;


%Places
array[1..number_of_places] of int: places_ID;
array[1..number_of_places] of int: places_category;


%Vehicules
int : number_of_vehicles;
array[1..number_of_vehicles] of int: vehicle_IDs;
array[1..number_of_vehicles] of int: capacity;
array[1..number_of_vehicles, 1..max_len] of int: can_Take;
array[1..number_of_vehicles, 1..max_len_availability] of int: vehicle_availability_start;
array[1..number_of_vehicles, 1..max_len_availability] of int: vehicle_availability_end;
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
int : first_vehicle = vehicle_IDs[1];
int : last_vehicle = vehicle_IDs[number_of_vehicles];
array[1..number_of_activities] of int: activities_patients_IDs;
array[1..number_of_activities] of var 0..1440: start_date;
array[1..number_of_activities] of var 0..1440: end_date;
array[1..number_of_activities] of int: start_location;
array[1..number_of_activities] of int: end_location;
array[1..number_of_activities] of int: duration_of_trip;
array[1..number_of_activities] of int: forward_or_backward;
array[1..number_of_activities] of var 0..1: executed_status;
array[1..number_of_activities] of var first_vehicle..last_vehicle: vehicle_assigned;
array[1..number_of_activities] of var int: trip_duration;
array[1..number_of_activities] of int: activities_load;



%Satisfied
array[1..number_of_activities] of var 0..1: samevehicle_satisfied;
array[1..number_of_activities] of var 0..1: category_satisfied;
array[1..number_of_activities] of var 0..1: horaire_satisfied;
array[1..number_of_activities] of var 0..1: availability_satisfied;

array[1..number_of_patients] of var 0..1: requests_accepted;

%DistMatrix
array[1..number_of_places, 1..number_of_places] of int : distMatrix;

constraint forall(i in 1..number_of_activities) (
  if forward_or_backward[i] == 1 then
    horaire_satisfied[i] = (
      (rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] > end_date[i]) /\
      ((rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] - max_wait_duration) < end_date[i]) /\
      (rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] > start_date[i]) /\
      ((rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] - max_wait_duration) < start_date[i])   
    )
  elseif forward_or_backward[i] == 0 then
    horaire_satisfied[i] = 
      ((rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] + rdv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]) < start_date[i]) /\
      ((rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] + rdv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] +  max_wait_duration) > start_date[i]) 
      /\
      ((rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] + rdv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]) < end_date[i]) /\
      ((rdv_time[activities_patients_IDs[i] - patients_IDs[1] + 1] + rdv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] +  max_wait_duration) > end_date[i])
   else 
     horaire_satisfied[i]=1
  endif
);

constraint forall(i in 1..number_of_activities) (
  start_date[i] = end_date[i] - trip_duration[i]
);

constraint forall(i in 1..number_of_activities)(
if forward_or_backward[i] != -1 then 
 trip_duration[i] > distMatrix[start_location[i]+1, end_location[i]+1]+2*srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]
endif);


constraint forall(i in 1..number_of_activities) (
    category_satisfied[i] = 
        (exists(j in 1..max_len) (
            can_Take[vehicle_assigned[i] - vehicle_IDs[1] + 1, j] = patients_category[activities_patients_IDs[i] - patients_IDs[1] + 1]
        ))
);

constraint forall(i in 1..number_of_activities) (
  if max_len_availability==1 /\ forward_or_backward[i] != -1 then
availability_satisfied[i] =(
  (start_date[i]>=vehicle_availability_start[vehicle_assigned[i]-vehicle_IDs[1]+1,1]+ distMatrix[starting_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],start_location[i]+1]) /\ end_date[i] <= vehicle_availability_end[ vehicle_assigned[i]-vehicle_IDs[1]+1,1]-distMatrix[ending_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],end_location[i]+1])
  
  elseif max_len_availability==2 /\ forward_or_backward[i] != -1 then
  availability_satisfied[i] =(
  (start_date[i]>=vehicle_availability_start[vehicle_assigned[i]-vehicle_IDs[1]+1,1]+ distMatrix[starting_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],start_location[i]+1] /\ end_date[i] <= vehicle_availability_end[ vehicle_assigned[i]-vehicle_IDs[1]+1,1]-distMatrix[ending_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],end_location[i]+1]
  \/ 
  (start_date[i]>=vehicle_availability_start[vehicle_assigned[i]-vehicle_IDs[1]+1,2]+ distMatrix[starting_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],start_location[i]+1]) /\ end_date[i] <= vehicle_availability_end[ vehicle_assigned[i]-vehicle_IDs[1]+1,2]-distMatrix[ending_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],end_location[i]+1]))
  
  elseif max_len_availability==3 /\ forward_or_backward[i] != -1 then
  availability_satisfied[i] =(
  (start_date[i]>=vehicle_availability_start[vehicle_assigned[i]-vehicle_IDs[1]+1,1]+ distMatrix[starting_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],start_location[i]+1] /\ end_date[i] <= vehicle_availability_end[ vehicle_assigned[i]-vehicle_IDs[1]+1,1]-distMatrix[ending_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],end_location[i]+1]
  \/ 
  (start_date[i]>=vehicle_availability_start[vehicle_assigned[i]-vehicle_IDs[1]+1,2]+ distMatrix[starting_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],start_location[i]+1]) /\ end_date[i] <= vehicle_availability_end[ vehicle_assigned[i]-vehicle_IDs[1]+1,2]-distMatrix[ending_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],end_location[i]+1])
  \/
  (start_date[i]>=vehicle_availability_start[vehicle_assigned[i]-vehicle_IDs[1]+1,3]+ distMatrix[starting_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],start_location[i]+1] /\ end_date[i] <= vehicle_availability_end[ vehicle_assigned[i]-vehicle_IDs[1]+1,3]-distMatrix[ending_depot[vehicle_assigned[i]-vehicle_IDs[1]+1],end_location[i]+1]))
  
  else availability_satisfied[i]=1
  
endif);
  

constraint forall(i in 1..number_of_activities where forward_or_backward[i] != -1)(
  samevehicle_satisfied[i] =
    forall(j in i+1..number_of_activities where (vehicle_assigned[i] == vehicle_assigned[j] /\ forward_or_backward[j] != -1)) (
      start_date[j]-start_date[i] >= distMatrix[start_location[i]+1,start_location[j]+1]+ srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] \/ start_date[i]-start_date[j] >= distMatrix[start_location[j]+1,start_location[i]+1]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1]
  /\
  start_date[j]-end_date[i] >= distMatrix[end_location[i]+1,start_location[j]+1] \/ end_date[i]-start_date[j] >= distMatrix[start_location[j]+1,end_location[i]+1]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1]+srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]
  /\
  end_date[j]-start_date[i] >= distMatrix[start_location[i]+1,end_location[j]+1]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1]+srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1] \/ start_date[i]-end_date[j] >= distMatrix[end_location[j]+1,start_location[i]+1]
  /\
  end_date[j]-end_date[i] >= distMatrix[end_location[i]+1,end_location[j]+1]+ srv_duration[activities_patients_IDs[j] - patients_IDs[1] + 1] \/ end_date[i]-end_date[j] >= distMatrix[end_location[j]+1,end_location[i]+1]+ srv_duration[activities_patients_IDs[i] - patients_IDs[1] + 1]
));


constraint forall(v in 1..number_of_vehicles)(
  cumulative(start_date, 
            [duration_of_trip[i] * bool2int(v = vehicle_assigned[i])| i in 1..number_of_activities] ,
            activities_load ,capacity[v]));

constraint forall(i in 1..number_of_activities)(
    executed_status[i] = (horaire_satisfied[i] == 1 /\
                          category_satisfied[i] == 1 /\
                          samevehicle_satisfied[i] == 1 /\
                          availability_satisfied[i] == 1)
);

constraint forall(i in 0..number_of_patients-1)(
  requests_accepted[i+1] = (executed_status[1+2*i]==1/\executed_status[2+2*i]==1)
  );


 
solve maximize sum(requests_accepted);
output ["{\"executed_status\": ", show(executed_status), ",\n"];
output ["\"forward_or_backward\": ", show(forward_or_backward), ",\n"];
output ["\"start_date\": ", show(start_date), ",\n"];
output ["\"end_date\": ", show(end_date), ",\n"];
output ["\"vehicle_assigned\": ", show(vehicle_assigned), ",\n"];
output ["\"requests_accepted\": ", show(requests_accepted), ",\n"];
output ["\"start_location\": ", show(start_location), ",\n"];
output ["\"end_location\": ", show(end_location), ",\n"];
output ["\"activities_patients_IDs\": ", show(activities_patients_IDs), ",\n"];
output ["\"starting_depot\": ", show(starting_depot), ",\n"];
output ["\"ending_depot\": ", show(ending_depot), ",\n"];
output ["\"vehicle_IDs\": ", show(vehicle_IDs), ",\n"];
output ["\"srv_duration\": ", show(srv_duration), ",\n"];
output ["\"vehicle_IDs\": ", show(vehicle_IDs), ",\n"];
output ["\"activities_load\": ", show(activities_load), ",\n"];
output ["\"patients_IDs\": ", show(patients_IDs), "}\n"];
