import frappe
from frappe import _
import pymssql
import pandas as pd
 
@frappe.whitelist()
def SyncTestResults(patient_id):
    conn_details = frappe.conf.biolis_server_connection
    if not patient_id:
            frappe.throw(_("Patient ID not found from barcode"))
    conn = pymssql.connect(
        conn_details["server"],
        conn_details["user"],
        conn_details["password"],
        conn_details["database"],
        timeout=30
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT
                ITEM_NAME,
                RESULT,
                PATI_ID,
                SAMP_ID,
                RDATE
                FROM
                    dbo.ResultLog
                WHERE
                PATI_ID = '{}'""".format(patient_id))
            
            rows = cursor.fetchall()
            
    except Exception as ex:
        print("Error: ", ex)
    conn.close()
    # patient_id = '221003.01'

    columns = ["ITEM_NAME","RESULTS", "PATI_ID","SAMP_ID","RDATE"]
    df = pd.DataFrame(rows, columns=columns)
    # result_values = df.to_dict('records')
    # df = pd.read_csv("/home/kishan/Desktop/result.csv")
    if df.empty:
        result_values = None
    else:
        # latest_samp_id = df[df['PATI_ID'] == patient_id].sort_values('RDATE', ascending=False).iloc[0]['SAMP_ID']
        # latest_data = df[df['SAMP_ID'] == latest_samp_id]
        # result_values = latest_data.to_dict('records')
        df = df.sort_values(['RDATE', 'SAMP_ID'], ascending=[True, True])
        df = df.drop_duplicates(subset='ITEM_NAME', keep='first')
        result_values = df.to_dict('records')   

    # frappe.msgprint(_(f"Test Result Synced for patient id : {patient_id}"), alert=True)
    return result_values