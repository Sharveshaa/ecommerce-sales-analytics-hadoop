# E-Commerce Sales Analytics Using Apache Hadoop

An end-to-end Big Data Analytics project that processes e-commerce transaction data using **Apache Hadoop, HDFS, YARN, Python MapReduce, and Docker**, with an interactive **Streamlit dashboard** for data visualization.

## Project Overview

This project analyzes **10,000 synthetic e-commerce transactions** and generates meaningful business insights across five dimensions:

- Product-wise revenue analysis
- Region-wise sales analysis
- Category-wise revenue analysis
- Monthly sales trend analysis
- Payment method analysis

The project demonstrates how distributed data processing can be implemented using the Hadoop ecosystem and visualized through an interactive dashboard.

## Objectives

- Set up a Hadoop environment using Docker containers.
- Store and manage transaction data using HDFS.
- Process large datasets using Hadoop MapReduce.
- Implement custom Mapper and Reducer programs using Python.
- Execute MapReduce jobs through YARN.
- Visualize analytical results using Streamlit.

## Technology Stack

| Technology | Purpose |
|---|---|
| Apache Hadoop 3.5.0 | Distributed data processing |
| HDFS | Distributed file storage |
| YARN | Resource and job management |
| Python 3 | Mapper and Reducer implementation |
| Hadoop Streaming | Execute Python MapReduce programs |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Matplotlib | Data visualization |

## System Architecture

The project uses four Docker containers to run a single-host, multi-container Hadoop cluster.

```text
              E-Commerce Dataset
                  (sales.csv)
                       |
                       v
                +-------------+
                |    HDFS     |
                |  NameNode   |
                +-------------+
                       |
                       v
                +-------------+
                |  DataNode   |
                +-------------+
                       |
                       v
              +------------------+
              |   YARN           |
              | ResourceManager  |
              +------------------+
                       |
                       v
              +------------------+
              |   NodeManager    |
              | MapReduce Tasks  |
              +------------------+
                       |
                       v
              +------------------+
              | Python Mapper    |
              | Python Reducer   |
              +------------------+
                       |
                       v
              +------------------+
              | HDFS Output      |
              | Analytics Results|
              +------------------+
                       |
                       v
              +------------------+
              | Streamlit        |
              | Dashboard        |
              +------------------+
```

## Hadoop Cluster Configuration

The Hadoop cluster consists of four containers:

| Container | Responsibility |
|---|---|
| NameNode | Manages HDFS metadata |
| DataNode | Stores HDFS data blocks |
| ResourceManager | Manages cluster resources |
| NodeManager | Executes processing tasks |

### Hadoop Web Interfaces

| Component | URL |
|---|---|
| NameNode | http://localhost:9870 |
| DataNode | http://localhost:9864 |
| ResourceManager | http://localhost:8088 |
| NodeManager | http://localhost:8042 |

## Dataset Description

The project uses a synthetic e-commerce dataset containing **10,000 transactions** generated using Python.

**Dataset columns:**

| Column | Description |
|---|---|
| OrderID | Unique transaction ID |
| Date | Transaction date |
| Product | Product name |
| Category | Product category |
| Quantity | Number of units purchased |
| Price | Unit price |
| Region | Sales region |
| PaymentMode | Payment method |

The dataset covers transactions from January 2025 to December 2025.

## MapReduce Implementation

Python Mapper and Reducer programs are executed using Hadoop Streaming.

### Mapper

The Mapper processes each transaction and generates key-value pairs for five analytical dimensions:

- PRODUCT
- REGION
- CATEGORY
- MONTH
- PAYMENT

It calculates revenue using:

`Revenue = Quantity × Price`

### Reducer

The Reducer receives grouped key-value pairs and calculates:

- Total revenue
- Total quantity sold
- Number of transaction records

The final output contains aggregated results across all five dimensions.

## Execution Results

The Hadoop MapReduce job completed successfully.

| Metric | Result |
|---|---:|
| Input transactions | 10,000 |
| Map output records | 50,000 |
| Reduce input records | 50,000 |
| Reduce output records | 38 |
| Map tasks launched | 2 |
| Reduce tasks launched | 1 |
| Failed shuffles | 0 |

### Key Business Insights

| Analysis | Highest Result |
|---|---|
| Top Revenue Product | Laptop |
| Top Revenue Category | Electronics |
| Top Revenue Region | South |
| Top Revenue Payment Mode | UPI |
| Top Revenue Month | May 2025 |

**Overall project statistics:**

- Total Revenue: ₹33.12 Crore
- Total Transactions: 10,000
- Total Units Sold: 29,951
- Average Transaction Value: ₹33,123.77

## Streamlit Dashboard

An interactive dashboard was developed using Streamlit to visualize the MapReduce output.

Dashboard features include:

- Key performance indicators (KPIs)
- Product-wise revenue visualization
- Monthly sales trend analysis
- Region-wise sales comparison
- Category-wise revenue distribution
- Payment method analysis
- Interactive filters
- Downloadable analytical results

## Project Directory Structure

```text
ecommerce-sales-analytics-hadoop/
│
├── config/
│   ├── core-site.xml
│   ├── hdfs-site.xml
│   ├── mapred-site.xml
│   └── yarn-site.xml
│
├── data/
│
├── scripts/
│   ├── mapper.py
│   └── reducer.py
│
├── output/
│
├── docker-compose.yml
├── generate_data.py
├── sales.csv
├── analytics_results.txt
├── dashboard.py
├── README.md
└── .gitignore
```

## How to Run the Project

### Prerequisites

- Windows
- Docker Desktop
- WSL2
- Python 3
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sharveshaa/ecommerce-sales-analytics-hadoop.git
```

### Step 2: Navigate to the Project

```bash
cd ecommerce-sales-analytics-hadoop
```

### Step 3: Start the Hadoop Cluster

```bash
docker compose up -d
```

### Step 4: Generate the Dataset (Optional)

```bash
python generate_data.py
```

### Step 5: Upload Dataset to HDFS

```bash
docker exec namenode hdfs dfs -mkdir -p /sales/input_large
```

```bash
docker cp sales.csv namenode:/tmp/sales.csv
```

```bash
docker exec namenode hdfs dfs -put /tmp/sales.csv /sales/input_large/
```

### Step 6: Run the MapReduce Job

Copy the Mapper and Reducer scripts into the ResourceManager container:

```bash
docker cp scripts/mapper.py resourcemanager:/tmp/mapper.py
docker cp scripts/reducer.py resourcemanager:/tmp/reducer.py
```

Execute Hadoop Streaming:

```bash
docker exec namenode hdfs dfs -rm -r -f /sales/analytics_output_v2
```

```bash
docker exec resourcemanager hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.5.0.jar -files /tmp/mapper.py,/tmp/reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input /sales/input_large/sales.csv -output /sales/analytics_output_v2
```

### Step 7: View the Results

```bash
docker exec namenode hdfs dfs -cat /sales/analytics_output_v2/part-00000
```

### Step 8: Run the Dashboard

Install the required Python packages:

```bash
pip install pandas matplotlib streamlit
```

Launch the dashboard:

```bash
python -m streamlit run dashboard.py
```

Open the dashboard at:

http://localhost:8501

## Future Enhancements

- Integrate Apache Hive for SQL-based analytics.
- Implement real-time transaction processing using Apache Kafka.
- Deploy the Hadoop cluster across multiple physical machines.
- Integrate predictive analytics and machine learning.
- Connect the dashboard to live data sources.

## Conclusion

This project demonstrates an end-to-end Big Data Analytics workflow using the Apache Hadoop ecosystem. It combines distributed storage, resource management, Python-based MapReduce processing, Docker containerization, and interactive data visualization to transform raw e-commerce transactions into meaningful business insights.

---

**Project:** E-Commerce Sales Analytics Using Apache Hadoop  
**Repository:** [GitHub](https://github.com/Sharveshaa/ecommerce-sales-analytics-hadoop)  
**Technologies:** Apache Hadoop | HDFS | YARN | Python | Docker | Streamlit
