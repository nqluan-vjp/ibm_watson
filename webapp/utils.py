'''
Created on 2020/06/29

@author: DXG
'''
import csv
import json
import os 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, "resources",'csv')
JSON_FOLDER = os.path.join(BASE_DIR, "resources",'json')

def convert_csv_to_json():
    with open(CSV_FOLDER + '/' + 'car_defects_info.csv' ,encoding="utf-8_sig") as f:
        list_data = []
        reader = csv.DictReader(f)
        for rows in reader:
            data = {}
            data['number'] = rows['番号']
            data['reception_date'] = rows['受付日']
            data['sex'] = rows['性別']
            data['address'] = rows['住所']
            data['method'] = rows['申告方法']
            data['car_name'] = rows['車名']
            data['common_name'] = rows['通称名']
            data['registration_date'] = rows['初度登録年月']
            data['total_mileage'] = rows['総走行距離']
            data['model'] = rows['型式']
            data['prime_mover_model'] = rows['原動機型式']
            data['defective_device'] = rows['不具合装置']
            data['time_of_emergence'] = rows['発生時期']
            data['summary'] = rows['申告内容の要約']    
            list_data.append(data)          
    with open(CSV_FOLDER + '/' + 'data.json', 'w' ,encoding="utf-8_sig") as f:
        f.write(json.dumps(list_data ,indent =4))
    with open(CSV_FOLDER + '/' + 'data.json','r',encoding="utf-8_sig") as in_json_file:
        doc_file = 1000
        json_obj_list = json.load(in_json_file)
        print(len(json_obj_list))
        for i in range(0, len(json_obj_list), doc_file):
            with open(JSON_FOLDER + '/' + 'data' +  str(i) + '.json', 'w') as outfile:
                outfile.write(json.dumps(json_obj_list[i:i+doc_file] ,indent =4))

