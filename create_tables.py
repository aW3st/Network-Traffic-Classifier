import pdb
import pandas as pd
import datetime as dt
import re
import os
import sys
from collections import OrderedDict
try: 
    path=sys.argv[1]+'/'
except:
    path=''

def mydateparser(x):
    x = pd.to_datetime(x, infer_datetime_format=True, errors='coerce')
    return x#.strftime("%Y-%m-%d %H:M%:S")

with open('../init.sql', 'w') as sqlfile:
    sqlfile.write('\connect trafficflow;\n')
    sqlfile.write('CREATE TABLE trafficdata(')
    column_types = OrderedDict() #use this to store column data type
    csv_list = []

    for csv in os.listdir():
        if re.match('.*\.csv', csv) is None:
            continue
        tablename = re.match('.*-2018', csv)[0]
        csv_list.append(tablename)
        print(csv_list)
        print('processing '+tablename)
        
        first_chunk=True
        chunks = pd.read_csv(csv, chunksize=600000, parse_dates=['Timestamp'], date_parser=mydateparser)
        for chunk in chunks:
            # delete duplicate header rows.
            chunk.drop(chunk.index[chunk['Dst Port']=='Dst Port'], inplace=True)
            chunk.drop(chunk.index[chunk['Timestamp'].dt.year!=2018],inplace=True)
            chunk.drop(['Flow ID', 'Src IP', 'Dst IP', 'Src Port'], axis=1, errors='ignore',inplace=True)
            assert len(chunk.columns) == 80
            chunk['Tablename'] = tablename
            if tablename==csv_list[0]:
                # add dtypes to dictionary if it's the first csv
                for index, dtype in enumerate(chunk.dtypes):
                    if chunk.columns[index] in ['Label','Dst Port', 'Protocol', 'Tablename']:
                        column_types[chunk.columns[index]]='TEXT'
                    elif chunk.columns[index]=='Timestamp':
                        column_types[chunk.columns[index]]='TIMESTAMP'
                    elif dtype == 'int64':
                        if chunk.columns[index]=='Flow Duration':
                            column_types[chunk.columns[index]]='BIGINT'
                        else:
                            column_types[chunk.columns[index]]='INT'
                    else:
                        column_types[chunk.columns[index]]='FLOAT'
            else:
                #if it's not the first csv, check that columns previously marked as int aren't floats
                for index, dtype in enumerate(chunk.dtypes):
                    if column_types[chunk.columns[index]]=='INT' and dtype != 'int64':
                        if dtype != 'object':
                            print(chunk.columns[index],' has different datatype: ', dtype)
                            column_types[chunk.columns[index]]='FLOAT'    
                        
            if first_chunk==True:
                # write first chunk with header
                chunk.to_csv('../'+path+tablename+'.csv', mode='w', index=False, header=True)
                first_chunk=False        
         
            else:
                # append subsequent chunks without header
                chunk.to_csv('../'+path+tablename+'.csv', index=False, mode='a', header=False)
    for column, dtype in column_types.items():
        #change spaces and forward slashes to underscores for postgres
        clean_col = column.replace(' ','_').replace('/','_')
        if clean_col == 'Tablename':
            sqlfile.write(clean_col+' TEXT);\n')
        else:
            sqlfile.write(clean_col+' '+dtype+',\n')
    for csv in csv_list:
        sqlfile.write('COPY trafficdata FROM \'/'+path+csv+'.csv\' CSV HEADER;\n')                    
           
        
