# Week 7 – Delta Lake Incremental Data Processing

## Objective

This assignment demonstrates incremental data processing using Delta Lake in Azure Databricks. It covers loading customer data, performing data cleaning, creating Delta tables, and applying MERGE operations to update existing records and insert new records.

---

## Technologies Used

- Azure Databricks
- Apache Spark (PySpark)
- Delta Lake
- Unity Catalog
- Python
- CSV Files

---

## Dataset

### Master Dataset
- customer_master.csv

Contains the initial customer records.

### Incremental Dataset
- customer_incremental.csv

Contains updated customer records along with new customers to simulate incremental data loading.

---

## Assignment Workflow

### Step 1
Load the master dataset into a Spark DataFrame.

### Step 2
Perform data cleaning:
- Handle null values
- Remove duplicate customer records
- Standardize string values

### Step 3
Create a Delta Table from the cleaned master dataset.

### Step 4
Load the incremental dataset.

### Step 5
Clean the incremental dataset:
- Replace null city values
- Remove duplicate customer IDs

### Step 6
Perform Delta MERGE (Upsert):
- Update existing customer records
- Insert new customer records

### Step 7
Validate results:
- Verify final row count
- Check duplicate records
- Display final dataset

---

## Folder Structure

```
delta-lake-assignment/
│
├── README.md
│
├── data/
│   ├── customer_master.csv
│   └── customer_incremental.csv
│
├── notebooks/
│   └── delta_scd_assignment.ipynb
│
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── scd1/
│   ├── scd2/
│   ├── validation/
│   └── final_output/
│
└── report/
    └── assignment_summary.pdf (Optional)
```

---

## Key Concepts Covered

- Delta Lake
- Delta Tables
- MERGE (UPSERT)
- Incremental Data Processing
- Data Cleaning
- Duplicate Removal
- Null Value Handling
- Data Validation
- PySpark DataFrames

---

## Results

- Successfully loaded customer data into a Delta table.
- Cleaned master and incremental datasets.
- Removed duplicate customer records.
- Handled missing values.
- Updated existing customers using MERGE.
- Inserted new customer records.
- Validated final dataset and duplicate count.

---

## Learning Outcomes

Through this assignment, I gained hands-on experience with:

- Delta Lake architecture
- Incremental data loading
- MERGE operations in Delta Lake
- Data validation techniques
- Building scalable ETL workflows using PySpark and Databricks

---

## Author

**Tanvi Ballal**

Celebal Technologies – Data Engineering Internship

Week 7 Assignment