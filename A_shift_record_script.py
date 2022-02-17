import datetime
import openpyxl
import requests
import json
from configparser import ConfigParser
import argparse


def convert_to_wareki(y, m, d):
    """西暦の年月日を和暦の年に変換する."""
    WAREKI_START = {
    '令和': datetime.datetime(2019, 5, 1),
    '平成': datetime.datetime(1989, 1, 8),
    '昭和': datetime.datetime(1926, 12, 25)
    }
    
    try:
        y_m_d = datetime.datetime(y, m, d)
        if WAREKI_START['令和'] <= y_m_d:
            reiwa_year = WAREKI_START['令和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = 'R'
        elif WAREKI_START['平成'] <= y_m_d:
            reiwa_year = WAREKI_START['平成'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = 'H'
        elif WAREKI_START['昭和'] <= y_m_d:
            reiwa_year = WAREKI_START['昭和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = 'S'
        else:
            return '昭和以前'

        if year == 1:
            year = '元'
       
        return era_str + str(year)
    except ValueError as e:
        raise e

def get_this_month_sheet(file_path):
    wb = openpyxl.load_workbook(file_path)
    today = datetime.date.today()
    ware = convert_to_wareki(today.year, today.month, today.day)
    sheet_name = ware + '.' + str(today.month) + '月'
    sheet = wb[sheet_name]
    return wb, sheet

def write_list_2d(sheet, l_2d, start_row, start_col):
    for y, row in enumerate(l_2d):
        for x, cell in enumerate(row):
            sheet.cell(row=start_row+y, column=start_col+x, value=l_2d[y][x])

def get_kintone(url, api_token):
    """kintoneのレコードを1件取得する関数"""
    headers = {"X-Cybozu-API-Token": api_token}
    resp = requests.get(url, headers=headers)
    return resp

def create_insp_dict(resp):
    p_res = json.loads(resp.text)
    insp_dict = {}
    for i in range(len(p_res['records'])):
        insp_list = []
        insp_list.append(p_res['records'][i]['First_RT_room_inspection']['value'])
        insp_list.append(p_res['records'][i]['Third_RT_room_inspection']['value'])
        insp_dict[p_res['records'][i]['date']['value']] = insp_list
    return sorted(insp_dict.items())

def get_insp_list_2d(insp_dict):
    insp_list_2d = []
    for j in range(31):
        insp_list_2d.append([None, None])
    for date_and_p in insp_dict:
        index = int(date_and_p[0][-2:])
        insp_list_2d[index-1] = date_and_p[1]
    return insp_list_2d



def main():
    config = ConfigParser()
    config.read('config.ini')

    SUB_DOMAIN = config['KINTONE']['SUB_DOMAIN']
    APP_ID = config['KINTONE']['APP_ID']
    API_TOKEN = config['KINTONE']['API_TOKEN']

    QUERY_d = 'date = THIS_MONTH()'

    URL = f"https://{SUB_DOMAIN}.cybozu.com/k/v1/records.json?app={APP_ID}&query={QUERY_d}"
    

    insp = create_insp_dict(get_kintone(URL, API_TOKEN))
    insp_list_2d = get_insp_list_2d(insp)
    wb, sheet = get_this_month_sheet(file_path='duty.xlsx')
    write_list_2d(sheet, insp_list_2d, 5, 7)
    wb.save("duty_A_shift_add.xlsx")



if __name__ == '__main__':
    main()





