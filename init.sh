#! /bin/bash
PORT=9999

while getopts ":h:p" opt; do
    case {$opt} in 
        h )
            echo "Creates docker container hosting network traffic database."
            echo "Port number may be specified with the -p flag (default 9999)."
            ;;
        p )
            PORT=$OPTARG
            ;;
        \? )
            echo "invalid argument: -$OPTARG" 1>&2
            ;;
    esac
done

mkdir clean_data
aws s3 sync --no-sign-request "s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms" data
cd data
python ../create_tables.py clean_data
cd ..
echo "building docker image..."
sudo docker build -t nettrafficdb .
echo "creating database container..."
sudo docker run --rm --name NetTrafficClassifier -p $PORT:5432 -v "$(pwd)"/clean_data:/clean_data nettrafficdb
echo "database now listening on port $PORT"

