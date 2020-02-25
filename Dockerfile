FROM python:3.7 as stage1
COPY create_tables.py .
WORKDIR data
RUN apt update &&\
mkdir ../clean_data &&\
apt install awscli -y &&\ 
pip install pandas numpy  &&\
aws s3 cp --no-sign-request "s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Friday-02-03-2018_TrafficForML_CICFlowMeter.csv" . &&\
aws s3 cp --no-sign-request "s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Friday-16-02-2018_TrafficForML_CICFlowMeter.csv" . 
RUN python ../create_tables.py

FROM postgres
ENV POSTGRES_DB=trafficflow
ENV POSTGRES_USER=docker
ENV POSTGRES_PASSWORD=mypass 
COPY --from=stage1 /clean_data /clean_data
COPY --from=stage1 init.sql /docker-entrypoint-initdb.d
CMD ["postgres"]
