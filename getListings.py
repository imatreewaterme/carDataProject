import requests
import json
import pyodbc

baseURL = 'https://auto.dev/api/'
method='listings'
make='&make=Subaru'
model='&model=BRZ'
#make='&make=Mazda'
#model='&model=MX-5%20Miata'

#yearMin='&year_min=2009'
#yearMax='&year_max=2015'
fullRequestUrl =baseURL+method+'?apikey=ZrQEPSkKcmNoaXAwODEyQGdtYWlsLmNvbQ=='+make+model

connPath = 'conn.txt'
with open(connPath, 'r') as file:
    conn = file.read()
print(conn)
def getListings ():
    x = 2
    #Initial Request#
    print(fullRequestUrl)
    response = requests.get(fullRequestUrl)
    if (response.status_code!=200):
        print("Request failed")
    else:
        data = json.loads(response.text)
        #Calculate number of pages needed to get all rows (20 rows per page are provided per api call)
        totalcount=data['totalCount']
        numPages = int(round(totalcount/20,0))
        cnxn = pyodbc.connect(conn)
        cursor = cnxn.cursor()
        print(numPages)
        while x <= 2:
        #while x <= numPages:
            page = '&page='+str(x)
            #Already has page 1 of data#
            if(x!=1):
                print(fullRequestUrl+page)
                response = requests.get(fullRequestUrl+page)
            if (response.status_code!=200):
                f = open("errorlog.txt", "a")
                f.write("Request failed on page: "+str(x))
                f.close()
                x += 1
            else:
                data = json.loads(response.text)
                for record in data['records']:
                    record['city']=str(record['city']).replace("'", "\'\'")
                    record['dealerName']=str(record['dealerName']).replace("'", "\'\'")
                    #query = "{}'{}'{}'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
                    query = "{}'{}'{}'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
                    "MERGE INTO carData AS target USING (SELECT ",
                    str(record['vin']),
                    " AS vin) AS source "
                    "ON target.vin = source.vin "
                    "WHEN NOT MATCHED THEN INSERT VALUES(",
                    str(record['id']),
                    str(record['vin']),
                    str(record['displayColor']),
                    str(record['year']),
                    str(record['make']),
                    str(record['model']),
                    record['dealerName'],
                    str(record['price']),
                    str(record['mileage']),
                    record['city'],
                    str(record['lat']),
                    str(record['lon']),
                    str(record['condition']),
                    str(record['createdAt']),
                    str(record['updatedAt']),
                    str(record['modelId']),
                    str(record['active']),
                    str(record['state']),
                    str(record['trim']),
                    str(record['bodyType']),
                    str(record['bodyStyle']),
                    str(record['regionName']),
                    str(record['experience']),
                    '''
                    "WHEN MATCHED THEN UPDATE VALUES("
                    str(record['displayColor']),
                    record['dealerName'],
                    str(record['price']),
                    str(record['mileage']),
                    record['city'],
                    str(record['lat']),
                    str(record['lon']),
                    str(record['condition']),
                    str(record['createdAt']),
                    str(record['updatedAt']),
                    str(record['active']),
                    str(record['state']),
                    str(record['bodyType']),
                    str(record['bodyStyle']),
                    str(record['regionName']),
                    str(record['experience'])
                    '''
                    )
                    '''
                    #Can be used to see how many duplicates we are getting#
                    query = "{}'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
                    "INSERT INTO carData2 VALUES(",
                    str(record['id']),
                    str(record['vin']),
                    str(record['displayColor']),
                    str(record['year']),
                    str(record['make']),
                    str(record['model']),
                    record['dealerName'],
                    str(record['price']),
                    str(record['mileage']),
                    record['city'],
                    str(record['lat']),
                    str(record['lon']),
                    str(record['condition']),
                    str(record['createdAt']),
                    str(record['updatedAt']),
                    str(record['modelId']),
                    str(record['active']),
                    str(record['state']),
                    str(record['trim']),
                    str(record['bodyType']),
                    str(record['bodyStyle']),
                    str(record['regionName']),
                    str(record['experience'])
                    )'
                    '''
                    #print(query)
                    cursor.execute(query)
                    cnxn.commit()
                    print("Inserting/Updating "+str(record['id']))
            x += 1

#Call
getListings()
