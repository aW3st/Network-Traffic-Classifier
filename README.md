# Network-Traffic-Classifier

Cyber crime causes [billions](https://www.internetsociety.org/news/press-releases/2019/internet-societys-online-trust-alliance-reports-cyber-incidents-cost-45b-in-2018/) of dollars in damages and results in millions of exposed personal records every year. Though hardly sufficient, machine learning forms an [important weapon](https://cloud.google.com/blog/products/g-suite/ridding-gmail-of-100-million-more-spam-messages-with-tensorflow) in our arsenal of defenses against criminals. This repo includes the **data prep, analysis, feature engineering, and model selection/training process** involved in building such a defense. The end result is a random forest classifier with an overal F-Score of 0.85, though poor performance in one class brought average scores down considerably. 

### Table of Contents

### Dataset

For such a critical problem to solve, there is a surprising paucity of abailable network traffic. Unsurprisingly, much network traffic consists of the most intimate (and, no doubt, the most banal) details of users' lives, and this intimacy precludes the publication of large, open datasets. In an attempt to fill this lack, the University of New Brunswick simulated the behavior of a 500-machine  network, carried out a variety of attacks, and collected the resulting network traffic and logs.  To facilitate research, they also released extracted features in csv-form. The resulting dataset is over **450 gigabytes** total, and the provided dataframes have over **50 million observations**.
![Network Topology](https://www.unb.ca/cic/_assets/images/cse-cic-ids2018.jpg "Network topology as implemented by UNB")

### Data Prep & Methodology

Due to the enormouse size of the dataset, we need a way to query the data from disk. For ease of access and replicability, I host the data on a postgres server run in a docker container. The init.sh shell script downloads the data, cleans it with pandas, builds the docker container, and then copies the data to the database. Just make sure you have docker and the packages in requirements.txt installed before running the script. 

### Results
TO DO
