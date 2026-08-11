# Healthcare Source Relationships

## Patients
Primary Key:
- patient_id

## Doctors
Primary Key:
- doctor_id

## Appointments
Primary Key:
- appointment_id

Foreign Keys:
- patient_id -> patients.patient_id
- doctor_id -> doctors.doctor_id

## Treatments
Primary Key:
- treatment_id

Foreign Keys:
- appointment_id -> appointments.appointment_id

## Billing
Primary Key:
- bill_id

Foreign Keys:
- patient_id -> patients.patient_id
- treatment_id -> treatments.treatment_id