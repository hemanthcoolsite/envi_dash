def datascraper(Bs_data):
    #f=open(file, 'r')
    #data = f.read()
    #Bs_data = BeautifulSoup(data, "xml")
    #all the values need to be collect
    env_n = Bs_data.find('project')
    env_n = env_n.get('name') if env_n != None else env_n
    
    ta_n = Bs_data.find('property', {'name':'ics.release'}).get('value')
    ocs_v = Bs_data.find('property', {'name':'ics_release_ocs'})
    ocs_v = ocs_v.get('value') if ocs_v != None else ocs_v
    
    wsc_v = Bs_data.find('property', {'name':'ics_release_wsc'})
    wsc_v = wsc_v.get('value') if wsc_v != None else wsc_v
    
    host_n = Bs_data.find('property', {'name':'host'}).get('value')
    db = Bs_data.find('property', {'name':'aaa_rdbms'})
    db = db.get('value') if db != None else db
    
    user = Bs_data.find('property', {'name':'os_username'}).get('value')
    psw = Bs_data.find('property', {'name':'os_password'}).get('value')
    
    cols=[env_n, ta_n, ocs_v, wsc_v, host_n, db, user, psw]
    #return the list object of dictionary
    return cols

from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as ps
from datetime import datetime
#import json
###
t_start1=datetime.now()
###
file_N = 'Envs_Details.csv'
f=open(file_N,'w',newline='')
var = csv.writer(f)
row_1st=['ENV_NAME','TA_VERSION','OCS_VERSION','WSC_VERSION','HOSTNAME','DB','USERNAME','PASSWORD']
var.writerow(row_1st)
####web driver to xml from web
opener = urllib.request.build_opener()
url='https://lausvn.temenosgroup.com/svn/devel/internal/ENV/Deployment/TA/ta_deployer/'
####
col_name = ["ENVS"]
link_path='inputlinks.csv' #paste path for thr asin file
df = ps.read_csv(link_path, names=col_name)
input_files =df.ENVS.to_list()
###
tlist=['Template/CIP_LX_VM_ORA2_ta_21.0.17.xml','Template/CIP_LX_VM_ORA2_tap_23.0.04_wsc1.3.01_mesi.xml']
for link in input_files:
    if '.xml' in link or '.template' not in link and '.txt' not in link:
        if link == 'Template/':
            for i in tlist:
                file = opener.open(url+i)
                res = file.read()
                file.close()
                data = BeautifulSoup(res)
                cols = datascraper(data.find('project')) 
                var.writerow(cols)
        else:
            file = opener.open(url+link)
                res = file.read()
                file.close()
                data = BeautifulSoup(res)
                cols = datascraper(data.find('project')) 
                var.writerow(cols)
    else:
        continue
f.close()
t_end=datetime.now()
print(f'computetion time#{comple_time = t_end-t_start1
}')