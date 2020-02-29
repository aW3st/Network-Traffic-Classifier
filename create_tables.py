import pdb
import pandas as pd
import datetime as dt
import re
import os
import sys

try: 
    path=sys.argv[1]+'/'
except:
    path=''

def mydateparser(x):
    x = pd.to_datetime(x, infer_datetime_format=True, errors='coerce')
    return x#.strftime("%Y-%m-%d %H:M%:S")

with open('../init.sql', 'w') as sqlfile:
    for csv in os.listdir():
        tablename = re.match('.*-2018', csv)
        if tablename is None:
            print('not a csv')
            continue
        tablename = re.sub('-','_',tablename[0])
        print('processing '+tablename)
        first=True
        if re.match('.*\.csv', csv):
            chunks = pd.read_csv(csv, chunksize=600000, parse_dates=['Timestamp'], date_parser=mydateparser)
            for chunk in chunks:
                chunk.drop(chunk.index[chunk['Dst Port']=='Dst Port'], inplace=True)
                chunk.drop(chunk.index[chunk['Timestamp'].dt.year!=2018],inplace=True)
                if first==True:
                    first=False
                    newcols = chunk.columns.str.replace(' ','_').str.replace('/','_')
                    chunk.to_csv('../'+path+tablename+'.csv', mode='w', index=False, header=True)
                    sqlfile.write('\connect trafficflow;\n')
                    sqlfile.write('CREATE TABLE '+tablename+'(\n')
                    for index, dtype in enumerate(chunk.dtypes):
                        if newcols[index]=='Label':
                            sqlfile.write('Label TEXT\n')
                        elif newcols[index] in ['Dst_Port', 'Protocol', 'Flow_ID', 'Src_Port', 'Src_IP', 'Dst_IP']:
                            sqlfile.write(newcols[index]+' TEXT,\n')
                        elif newcols[index]=='Timestamp':
                            sqlfile.write(newcols[index]+' TIMESTAMP,\n')
                        elif dtype == 'int64':
                            if newcols[index]=='Flow_Duration':
                                sqlfile.write(newcols[index]+ ' BIGINT,\n')
                            else:
                                sqlfile.write(newcols[index]+' INT,\n')
                        else:
                            sqlfile.write(newcols[index]+' FLOAT,\n')
                    sqlfile.write(');\nCOPY '+tablename+' FROM \'/'+path+tablename+'.csv\' CSV HEADER;\n')
                else:
                    chunk.to_csv('../'+path+tablename+'.csv', index=False, mode='a', header=False)


                    
           
