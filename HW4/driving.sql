CREATE TABLE Person (
    ssn INTEGER PRIMARY KEY,
    name VARCHAR(256)
);

CREATE TABLE Driver (
    driverID INTEGER,
    ssn INTEGER,
    FOREIGN KEY (ssn) REFERENCES Person(ssn)
);

CREATE TABLE NonProfessionalDriver (
    driverID INTEGER,
    FOREIGN KEY (driverID) REFERENCES Driver(driverID)
);

CREATE TABLE ProfessionalDriver (
    driverID INTEGER,
    medicalHistory VARCHAR(256),
    FOREIGN KEY (driverID) REFERENCES Driver(driverID)
);

CREATE TABLE InsuranceCo (
    name VARCHAR(256) PRIMARY KEY,
    phone INTEGER
);

CREATE TABLE Vehicle (
   licensePlate VARCHAR(256) PRIMARY KEY,
   year INTEGER,
   maxLiability REAL,
   ownerSSN INTEGER,
   insurCoName VARCHAR(256),  
   FOREIGN KEY (ownerSSN) REFERENCES Person(ssn), 
   FOREIGN KEY (insurCoName) REFERENCES InsuranceCo(name)
); 

CREATE TABLE Car (
  licensePlate VARCHAR(256),
  make VARCHAR(256),
  FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
); 

CREATE TABLE Truck (
  licensePlate VARCHAR(256),  
  capacity INTEGER,  
  FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
); 

-- b. Which relation in your relational schema represents the relationship "insures" in the E/R diagram? Why is that your representation?
-- It s represented by the Vehicle table in the relational schema which has a foreign key insurCoName that references the primary key name in the InsuranceCo table.
-- Because this is the representation because the insurance company insures the vehicle.


-- c. Compare the representation of the relationships "drives" and "operates" in your schema, and explain why they are different.
-- We need to make sure if the driver are professional driver, if yes, we need to add attribute medicalhistory data to "operate" trunk.
-- If the driver is not professional driver than only "drives" car.