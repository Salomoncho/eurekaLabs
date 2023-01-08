from rest_framework import status
from collections import OrderedDict
from datetime import datetime

from api import api_messages

AV_RES_KEYS = {
    'OPEN': '1. open',
    'HIGH': '2. high',
    'LOW': '3. low',
    'CLOSE': '4. close',
    'DATA': 'Time Series (Daily)',
    'WARNING': 'Note',
    'ERROR': 'Error Message'
}


def isfloat(num):
    if isinstance(num, str):
        return False
    try:
        float(num)
        return True
    except ValueError:
        return False


def format_two_digit(float_num):
    return '{:.2f}'.format(float_num) if isfloat(float_num) else float_num


def calculate_last_two_variation(second_last_of_the_range, last_of_the_range):
    last_two_closing_diff = float(last_of_the_range[AV_RES_KEYS['CLOSE']])\
                            - float(second_last_of_the_range[AV_RES_KEYS['CLOSE']])
    return format_two_digit((last_two_closing_diff / float(last_of_the_range[AV_RES_KEYS['CLOSE']])) * 100)


def output(stock_info, stock_info_keys):
    resp = OrderedDict()
    reversed_list = stock_info_keys[::]
    close_previous = stock_info.get(reversed_list[0])
    resp[stock_info_keys[0]] = {
        "Open Price": stock_info[reversed_list[0]][AV_RES_KEYS['OPEN']],
        "Higher price": stock_info[reversed_list[0]][AV_RES_KEYS['HIGH']],
        "Lower price": stock_info[reversed_list[0]][AV_RES_KEYS['LOW']],
        "Close price": stock_info[reversed_list[0]][AV_RES_KEYS['CLOSE']],
        "Variation Percentage": format_two_digit(0)
    }
    for i in range(1, len(reversed_list)):
        resp[stock_info_keys[i]] = {
            "Open Price": stock_info[reversed_list[i]][AV_RES_KEYS['OPEN']],
            "Higher price": stock_info[reversed_list[i]][AV_RES_KEYS['HIGH']],
            "Lower price": stock_info[reversed_list[i]][AV_RES_KEYS['LOW']],
            "Close price": stock_info[reversed_list[i]][AV_RES_KEYS['CLOSE']],
            "Variation Percentage": calculate_last_two_variation(close_previous, stock_info[reversed_list[i]])
        }
        close_previous = stock_info[reversed_list[i]]
    return resp


def process_alphavantage_data(data):
    stock_info_keys = list(data.keys())
    stock_info_keys.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d'))
    return output(data, stock_info_keys)


def validate_response(data):
    if AV_RES_KEYS['DATA'] in data:
        valid_data = data.get(AV_RES_KEYS['DATA'])
        return {'status': status.HTTP_200_OK, 'data': valid_data}
    else:
        return {'error': api_messages.INVALID_API_CALL, 'status': status.HTTP_400_BAD_REQUEST, 'data': None}
