# Week 4 – Azure Cloud Fundamentals and Data Pipeline Implementation using ADF

## Objective

The objective of this assignment was to understand Azure Cloud fundamentals and implement an end-to-end data pipeline using Azure Storage Account and Azure Data Factory (ADF). The pipeline reads a CSV file from Azure Blob Storage, validates metadata, and copies the data to a destination container.

---

## Tools Used

- Microsoft Azure Portal
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory (ADF)
- Azure IAM (Role-Based Access Control)
- Sample Superstore Dataset (CSV)

---

## Dataset

**Dataset Name:** Sample Superstore Dataset

The dataset contains sales transaction information including:

- Order ID
- Order Date
- Customer Name
- Segment
- Region
- State
- Product Category
- Product Name
- Sales
- Quantity
- Profit

The dataset was uploaded to Azure Blob Storage and used as the source file for the Azure Data Factory pipeline.

---

## Folder Structure

```
Week4/
│
├── data/
│   └── Sample-Superstore.csv
|
├── Azure_Cloud_Fundamentals_and_Data_Pipeline_Implementation_using_ADF.docx
│
└── README.md
```

---

## Steps Performed

1. Created a Resource Group.
2. Created an Azure Storage Account.
3. Created Blob Storage containers.
4. Uploaded the Sample Superstore CSV file.
5. Created Azure Data Factory.
6. Configured Linked Service for Blob Storage.
7. Created Source and Destination datasets.
8. Configured Get Metadata activity.
9. Built a Copy Data pipeline.
10. Executed and validated the pipeline.
11. Assigned IAM roles for secure resource access.

---

## Azure Services Used

- Resource Group
- Storage Account
- Blob Container
- Azure Data Factory
- Linked Services
- Datasets
- Copy Data Activity
- Get Metadata Activity
- IAM (Reader & Contributor)

---

## Learning Outcomes

- Understood Azure cloud resource management.
- Learned Blob Storage configuration.
- Connected Azure Storage with Azure Data Factory.
- Built a data pipeline using Copy Data activity.
- Performed metadata validation using Get Metadata.
- Explored Azure IAM role assignments and permissions.

---

## Conclusion

Successfully implemented an Azure-based data integration workflow by configuring Azure Storage and Azure Data Factory. The assignment provided practical experience in cloud storage, data movement, metadata validation, and pipeline orchestration.