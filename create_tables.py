import pdb
import pandas as pd
import numpy as np
import os
import re
pd.set_option('use_inf_as_na', True)

ls = os.listdir()
with open('../init.sql', 'w') as f:
    for csv in ls:
        match = re.search(r'.+(?=-2018)', csv)
        if match==None:
            continue
        tablename = match[0].replace('-','_')
        newcols = []
        df_out = pd.DataFrame()
        chunks = pd.read_csv(csv, chunksize=200000, parse_dates=['Timestamp'], date_parser=lambda x: pd.to_datetime(x, errors='coerce',yearfirst=True, format='%d/%m/%Y %H:%M:%S'))
        first = True
        print('tablename: ',tablename)
        for chunk in chunks:
            chunk.drop(chunk[chunk['Dst Port']=='Dst Port'].index, inplace=True)
           # for name, series in chunk.items():
           #     if series.dtype.name!='category'
           #         chunk[name]= pd.to_numeric(series, errors='coerce')
            df_out = pd.concat([df_out, chunk])
            if first:
                df_out.to_csv('../clean_data/'+tablename+'.csv', mode='w', header=True, index=False)
                newcols = chunk.columns.str.replace(' ','_').str.replace('/','_')
                f.write('\connect trafficflow\n')
                f.write('CREATE TABLE '+tablename+'(\n')
                for index, dtype in enumerate(chunk.dtypes):
                    if newcols[index]=='Label':
                        f.write('Label TEXT\n')
                    elif newcols[index] in ['Dst_Port','Protocol']:
                        f.write(newcols[index]+' TEXT,\n')
                    elif newcols[index]=='Timestamp':
                        f.write('Timestamp TIMESTAMP,\n')
                    elif dtype.name=='str':
                        f.write(newcols[index]+' TEXT,\n')
                    elif dtype=='int64':
                        f.write(newcols[index]+' integer,\n')
                    else:
                        f.write(newcols[index]+' FLOAT,\n')
                f.write(');\nCOPY '+tablename+' FROM \'/clean_data/'+tablename+'.csv\' CSV HEADER;\n')
                first = False
            else:
                df_out.to_csv('../clean_data/'+tablename+'.csv', mode='a', header=False, index=False)
