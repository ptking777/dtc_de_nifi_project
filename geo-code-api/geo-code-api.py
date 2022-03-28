import urllib.parse
import os
import csv
import sys
import urllib.request
import json
from jsonpath_ng import jsonpath, parse
import traceback


USAGE = f"USAGE: {sys.argv[0]} <input file>"

def main():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
  
    if (len(sys.argv) > 1 ):
       filename = sys.argv[1]
       print(f"filename: {filename}")
    else:
       filename = "invalid"
       print(f"filename: {filename}")
       print("Terminating...")
       raise AssertionError(USAGE)

    key =  os.environ['GCP_API_KEY']



    # opening the CSV file
    with open(filename, mode ='r') as file:
   
       # reading the CSV file
       csvFile = csv.reader(file, delimiter = "|")

       # displaying the contents of the CSV file
       header = next(csvFile)
       jsonpath_expression = parse('$.plus_code.compound_code')
       
       with open("./output.txt", mode = 'w') as output:

           for lines in csvFile:
               if (len(lines) > 0):
                 (lat,lon) = (lines)
     
                 the_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&location_type=ROOFTOP&result_type=street_address&key=" 
                 the_url = the_url + key
                 
                 # query api
                 get_url = urllib.request.urlopen(the_url)
                 #print("Response Status: "+ str(get_url.getcode()) )
                 retcode = get_url.getcode()
                 if (retcode == 200):
                     result = get_url.read()
                     json_data = json.loads(result) 
                     #status = json_data['status']
                     try:
                         error_message = json_data.get('error_message')
                         if (error_message != None):
                           print(f"status: {status}")
                           print(f"error_message: {error_message}")
                           continue
                     except NameError:
                         pass

                     match = jsonpath_expression.find(json_data)
                     if (len(match) < 1 ):
                         continue
                     location = match[0].value
                     x = location.find(" ")
                     x = x + 1
                     #print(match)
                     locality = location[x:]
                     locality = locality.strip()
                     data = dict()
                     data['locality'] = locality
                     data['latitude'] = lat
                     data['longitude'] = lon
                     #print(json.dumps(data))
                     output.writelines([json.dumps(data),"\n"])
                 else:
                     print(f"ERROR: Request Failed {retcode}")
                     
                     #print(f"locality:{locality},lat:{lat},lon:{lon}")
                 
  
if __name__ == "__main__":
    try:
       main()
  
    except Exception as error: 
        print(traceback.format_exc()) 
        #print('Caught this error: ' + repr(error))
        # print("Gotcha!")


