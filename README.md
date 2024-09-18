# Search and Planning 2023/24 - Patient Transportation Problem as a CSP

## Project Overview
This project aims to develop an encoding to solve the Patient Transportation Problem (PTP) as a Constraint Satisfaction Problem (CSP).

### Problem Specification
As per problem 082 in CSPlib, the PTP involves transporting patients to medical appointments using a heterogeneous fleet of vehicles. The fleet includes ambulances and volunteer private drivers. Each patient request has specific characteristics.

#### Decision Aspects
The PTP involves:
1. Selecting which requests to service.
2. Assigning vehicles to requests.
3. Routing and scheduling vehicles appropriately.

#### Specific Characteristics
- Patients have various constraints (e.g., maximum travel/waiting time).
- Requests vary (e.g., single/return trips, multiple passengers).
- Vehicle fleet differences (capacity, location, availability).
- Non-continuous vehicle availability (specific time slots).

### Problem Nature
- Static version: All requests known beforehand, no real-time additions.

### Example Illustration
An illustration with a single vehicle and two patients (A and B) is provided. The sequence involves taking A to hospital A, then taking B, followed by returning A with B, dropping A, taking B to hospital B, and finally dropping B.

![PTP Illustration](C:\Users\pauld\Downloads\Capture.png)

---

## Repository Contents
- `code/`: Contains the implementation code.

### Project Structure
The project structure is designed to organize code, data, and results.

---

## Instructions
Detailed instructions for the project will be provided in the respective code files or documentation. 

---
