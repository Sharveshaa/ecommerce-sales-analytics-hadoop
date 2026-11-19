\# E-Commerce Sales Analytics Using Apache Hadoop



An end-to-end Big Data Analytics project that processes e-commerce transaction data using Apache Hadoop, HDFS, YARN, Python MapReduce and Docker, with an interactive Streamlit dashboard for visualization.



\## Project Overview



This project analyzes 10,000 synthetic e-commerce transactions and generates insights across five dimensions:



\- Product-wise revenue analysis

\- Region-wise sales analysis

\- Category-wise revenue analysis

\- Monthly sales trends

\- Payment method analysis



\## System Architecture



```text

Python Data Generation

&#x20;       |

&#x20;       v

&#x20;   sales.csv

&#x20;       |

&#x20;       v

&#x20;  HDFS Storage

&#x20;       |

&#x20;       v

&#x20;YARN Resource Management

&#x20;       |

&#x20;       v

&#x20;Hadoop Streaming

&#x20;       |

&#x20;       v

&#x20;   Mapper.py

&#x20;       |

&#x20;       v

&#x20; Shuffle and Sort

&#x20;       |

&#x20;       v

&#x20;   Reducer.py

&#x20;       |

&#x20;       v

&#x20;HDFS Analytics Output

&#x20;       |

&#x20;       v

&#x20;Streamlit Dashboard

```



\## Project Directory



```text

hadoop-lab/

├── config/

│   ├── core-site.xml

│   ├── hdfs-site.xml

│   ├── mapred-site.xml

│   └── yarn-site.xml

├── scripts/

│   ├── mapper.py

│   └── reducer.py

├── data/

├── output/

├── generate\_data.py

├── sales.csv

├── analytics\_results.txt

├── dashboard.py

├── docker-compose.yml

└── README.md

```



\## Technology Stack



\- Apache Hadoop 3.5.0

\- HDFS

\- YARN

\- Hadoop Streaming

\- Python 3

\- Docker and Docker Compose

\- Pandas

\- Matplotlib

\- Streamlit



\## Dataset



\- 10,000 synthetic transactions

\- 8 attributes

\- 12 products

\- 4 categories

\- 5 regions

\- 5 payment methods

\- Date range: January 2025 to December 2025



\## MapReduce Processing



Each transaction generates five intermediate key-value records.



10,000 transactions × 5 records = 50,000 mapper records.



The reducer aggregates revenue, quantity and transaction counts, producing 38 analytical results.



\## Results



\- Total transactions: 10,000

\- Total revenue: ₹33,12,37,700

\- Total units sold: 29,951

\- Mapper output records: 50,000

\- Reducer output records: 38

\- Map tasks: 2

\- Reduce tasks: 1

\- MapReduce job completed successfully.



\## Running the Project



Start the Hadoop containers:



```bash

docker compose up -d

```



Run the Streamlit dashboard:



```bash

python -m streamlit run dashboard.py

```



Open:



http://localhost:8501



Hadoop web interfaces:



\- NameNode: http://localhost:9870

\- ResourceManager: http://localhost:8088



\## Deployment Note



The Hadoop services run in separate Docker containers on a single physical machine. This is a single-host, multi-container Hadoop deployment.



\## Author



Your Name



\## License



This project is available for educational purposes.

