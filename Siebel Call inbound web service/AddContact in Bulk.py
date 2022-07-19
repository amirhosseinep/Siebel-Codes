import requests
import json
import csv
import pandas
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def result2CSV(p_ServiceNumber, p_Birthdate, p_FirstName, p_LastName, p_Status, p_Type, p_BillId, p_Gender, resp_CreateContact, fileCSV):
    data = json.loads(resp_CreateContact.text)
    #print(data)
    for s in ("ServiceNumber","Birthdate","FirstName","LastName","Status","Type","BillId","Gender","ResponseDescription", "ResponseCode"):
        try:
            data[s]
        except:
            data[s] = '0'
    print(data)
    fileCSV.writerow([p_ServiceNumber,
                      p_Birthdate,
                      p_FirstName,
                      p_LastName,
                      p_Status,
                      p_Type,
                      p_BillId,
                      p_Gender,
                      data["ResponseDescription"],
                      data["ResponseCode"]])
    x=[p_ServiceNumber,
                      p_Birthdate,
                      p_FirstName,
                      p_LastName,
                      p_Status,
                      p_Type,
                      p_BillId,
                      p_Gender,
                      data["ResponseDescription"],
                      data["ResponseCode"]]

def CreateContact():
    url = 'https://***/siebel/v1.0/service/Contacts/CreateContact'
    contentType= {"Content-Type": "application/json"}

    p_ServiceNumber='9922118235'
    p_Birthdate='2/24/2010'
    p_FirstName='amir'
    p_LastName='pyt1'
    p_Status='2'
    p_Type='1'
    p_BillId='5208559'
    p_Gender='M'
    myReq = {"body": {
            "ServiceNumber": p_ServiceNumber,
            "Birthdate": p_Birthdate,
            "FirstName": p_FirstName,
            "LastName": p_LastName,
            "Status": p_Status,
            "Type": p_Type,
            "BillId": p_BillId,
            "Gender": p_Gender
                    }
            }
    resp_CreateContact = requests.post(url, verify=False, headers=contentType,auth=('sadmin', '***'), data=json.dumps(myReq))

    print (resp_CreateContact.content.decode("utf-8"))
    fileCSV = csv.writer(open("c:\\Siebel\\result_CreateContact_single.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(["ServiceNumber","Birthdate","FirstName","LastName","Status","Type","BillId","Gender","ResponseDescription", "ResponseCode"])
    result2CSV(p_ServiceNumber, p_Birthdate, p_FirstName, p_LastName, p_Status, p_Type, p_BillId, p_Gender, resp_CreateContact, fileCSV)


def BatchCreateContact():
    url = 'https://***/siebel/v1.0/service/Contacts/CreateContact'
    contentType = {"Content-Type": "application/json"}
    print(
        'Please make sure you have the CSV File with this name in below path: \nc:\Siebel\CreateContact.csv \n\nPress Enter to Continue...')
    #input()
    fileCSV = csv.writer(open("c:\\Siebel\\results_CreateContact.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(["ServiceNumber","Birthdate","FirstName","LastName","Status","Type","BillId","Gender","ResponseDescription", "ResponseCode"])
    df = pandas.read_csv('c:\\Siebel\\CreateContact.csv')

    row_column=df.shape #number of rows and columns
    print(row_column[0]) #number of rows

    for i in range(0,row_column[0]):
        p_ServiceNumber = str(df['ServiceNumber'][i])
        p_Birthdate = str(df['Birthdate'][i])
        p_FirstName = str(df['FirstName'][i])
        p_LastName = str(df['LastName'][i])
        p_Status = str(df['Status'][i])
        p_Type = str(df['Type'][i])
        p_BillId = str(df['BillId'][i])
        p_Gender = str(df['Gender'][i])

        myReq = {"body": {
            "ServiceNumber": p_ServiceNumber,
            "Birthdate": p_Birthdate,
            "FirstName": p_FirstName,
            "LastName": p_LastName,
            "Status": p_Status,
            "Type": p_Type,
            "BillId": p_BillId,
            "Gender": p_Gender
        }}
        print(myReq)
        try:
            resp_CreateContact = requests.post(url, verify=False, headers=contentType, auth=('sadmin', '***'), data=json.dumps(myReq),timeout=999999)
        except:
            print('Please check the network! \nYou can check the result path to see is there any results or not.\n\nPress Enter to Exit...')
            # time.sleep(5)
            input()
            sys.exit()

        print(resp_CreateContact.content.decode("utf-8"))
        result2CSV(p_ServiceNumber, p_Birthdate, p_FirstName, p_LastName, p_Status, p_Type, p_BillId, p_Gender, resp_CreateContact, fileCSV)

#CreateContact()
BatchCreateContact()

