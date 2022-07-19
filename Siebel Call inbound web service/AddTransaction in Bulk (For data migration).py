import requests
import json
import csv
import pandas

def result2CSV(p_MembershipNumber,p_ProductName,p_Amount,p_TransactionType, resp_RegisterProcessTnx, fileCSV):
    data = json.loads(resp_RegisterProcessTnx.text)
    #print(data)
    for s in ("MembershipNumber","ProductName","Amount","TransactionType", "TransactionStatus", "ResponseDescription", "ResponseCode", "TransactionSubStatus"):
        try:
            data[s]
        except:
            data[s] = '0'
    print(data)
    fileCSV.writerow([p_MembershipNumber,
                      p_ProductName,
                      p_Amount,
                      p_TransactionType,
                      data["TransactionStatus"],
                      data["ResponseDescription"],
                      data["ResponseCode"],
                      data["TransactionSubStatus"]])
    x=[p_MembershipNumber,
                      p_ProductName,
                      p_Amount,
                      p_TransactionType,
                      data["TransactionStatus"],
                      data["ResponseDescription"],
                      data["ResponseCode"],
                      data["TransactionSubStatus"]]

def RegisterProcessTnx():
    url = 'https://***/siebel/v1.0/service/LoyaltyProgramWebService/RegisterProcessTnx'
    contentType= {"Content-Type": "application/json"}

    p_MembershipNumber = "9927567871"
    p_ProductName = "2GB"
    p_Amount = "15"
    p_TransactionType =  "Accrual"
    myReq = {"body": {
        "MembershipNumber": p_MembershipNumber,
        "ProductName": p_ProductName,
        "Channel": "CFA",
        "Amount": p_Amount,
        "ProgramId": "9SIA-GQI6H",
        "TransactionType": p_TransactionType,
        "TransactionSubType": "Product"
                    }
        }
    resp_RegisterProcessTnx = requests.post(url, verify=False, headers=contentType,auth=('sadmin', '***'), data=json.dumps(myReq))

    print (resp_RegisterProcessTnx.content.decode("utf-8"))
    fileCSV = csv.writer(open("c:\\Siebel\\result_RegisterProcessTnx.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(["MembershipNumber","ProductName","Amount","TransactionType", "TransactionStatus", "ResponseDescription", "ResponseCode", "TransactionSubStatus"])
    result2CSV(p_MembershipNumber,p_ProductName,p_Amount,p_TransactionType, resp_RegisterProcessTnx, fileCSV)


def BatchRegisterProcessTnx():
    url = 'https://***/siebel/v1.0/service/LoyaltyProgramWebService/RegisterProcessTnx'
    contentType = {"Content-Type": "application/json"}
    print(
        'Please make sure you have the CSV File with this name in below path: \nc:\Siebel\BatchRegisterProcessTnx.csv \n\nPress Enter to Continue...')
    input()
    fileCSV = csv.writer(open("c:\\Siebel\\results_BatchRegisterProcessTnx.csv", "w+", newline='', encoding='utf-8'))
    fileCSV.writerow(
        ["MembershipNumber","ProductName","Amount","TransactionType", "TransactionStatus", "ResponseDescription", "ResponseCode", "TransactionSubStatus"])
    df = pandas.read_csv('c:\\Siebel\\BatchRegisterProcessTnx.csv')

    row_column=df.shape #number of rows and columns
    print(row_column[0]) #number of rows

    for i in range(0,row_column[0]):
        p_MembershipNumber = str(df['MembershipNumber'][i])
        p_ProductName = str(df['ProductName'][i])
        p_Channel = str(df['Channel'][i])
        p_Amount = str(df['Amount'][i])
        p_ProgramId = str(df['ProgramId'][i])
        p_TransactionType = str(df['TransactionType'][i])
        p_TransactionSubType = str(df['TransactionSubType'][i])

        myReq = {"body": {
            "MembershipNumber": p_MembershipNumber,
            "ProductName": p_ProductName,
            "Channel": p_Channel,
            "Amount": p_Amount,
            "ProgramId": p_ProgramId,
            "TransactionType": p_TransactionType,
            "TransactionSubType": p_TransactionSubType
        }}
        print(myReq)
        try:
            resp_BatchRegisterProcessTnx = requests.post(url, verify=False, headers=contentType, auth=('sadmin', '***'),
                                            data=json.dumps(myReq))
        except:
            print('Please check the network! \nYou can check the result path to see is there any results or not.\n\nPress Enter to Exit...')
            # time.sleep(5)
            input()
            sys.exit()

        print(resp_BatchRegisterProcessTnx.content.decode("utf-8"))
        result2CSV(p_MembershipNumber, p_ProductName, p_Amount, p_TransactionType, resp_BatchRegisterProcessTnx, fileCSV)


#RegisterProcessTnx()
BatchRegisterProcessTnx()

