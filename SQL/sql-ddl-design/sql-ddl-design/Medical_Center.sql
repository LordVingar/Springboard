-- Doctors table
CREATE TABLE Doctors (
    doctor_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    specialty TEXT
);

-- Patients table
CREATE TABLE Patients (
    patient_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE
);

-- Visits table
CREATE TABLE Visits (
    visit_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES Patients(patient_id),
    visit_date DATE NOT NULL,
    notes TEXT
);

-- Diseases table
CREATE TABLE Diseases (
    disease_id SERIAL PRIMARY KEY,
    disease_name TEXT NOT NULL
);

-- Doctor_Patient table to handle the many-to-many relationship
CREATE TABLE Doctor_Patient (
    doctor_id INTEGER REFERENCES Doctors(doctor_id),
    patient_id INTEGER REFERENCES Patients(patient_id),
    PRIMARY KEY (doctor_id, patient_id)
);

-- Visit_Disease table to handle the many-to-many relationship
CREATE TABLE Visit_Disease (
    visit_id INTEGER REFERENCES Visits(visit_id),
    disease_id INTEGER REFERENCES Diseases(disease_id),
    PRIMARY KEY (visit_id, disease_id)
);