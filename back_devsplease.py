import pandas as pd
import requests
import json
import time

users_dict={}#not delete!!!!
name_dict={}#not delete!!!!

def extract_names_from_excel_file():
    '''
    The function extract names from excel file
    :return:
    '''
    df_names = pd.read_excel(r'israel_names.xlsx')
    df_names = df_names['Column3']
    list_names = df_names.values.tolist()
    return list_names

def insert_users_dict(dict_response,item_index,flag):#not delete!!!!!
    '''

    :param dict_response: dict to insert
    :param item_index: key of dict
    :param flag: 0 or 1 accroding to type dict
    :return:
    '''
    global users_dict,name_dict
    if flag==0:#insert_dict_to_general_dict
        if dict_response[item_index] not in users_dict.values():
            users_dict[len(users_dict.keys())]=dict_response[item_index]
            print( users_dict[len(users_dict.keys())])
    if flag==1:#insert to temp_dict_with_more_10,000_result
        if dict_response[item_index] not in name_dict.values():
            name_dict[len(name_dict.keys())]=dict_response[item_index]
            print(name_dict[len(name_dict.keys())])


def basic_search(name, page):
    '''

    :param name:
    :param page:
    :return:
    '''
    url = "https://api.github.com/search/users?q=" + str(name) + "&page=" + str(page) + "&per_page=100"
    payload = {}
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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',
        'X-GitHub-Api-Version': '2022-11-28',
        'Cookie': 'logged_in=no'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except:
        time.sleep(60)
        basic_search(name, page)
    str_response = response.text
    dict_response = json.loads(str_response)
    if not (dict_response['items']):  # if dict_items is empty
        return None
    else:
        if dict_response['total_count'] > 1000:  # pass to search big data(>10,000)
            new_search(name, page)
        else:  # insert users_dict with data from current page
            for value in dict_response['items']:
                insert_users_dict(dict_response['items'], dict_response['items'].index(value), 0)
            basic_search(name, page + 1)


def new_search(name, page):
    '''

    :param name:
    :param page:
    :return:
    '''
    order_list = ['desc', 'asc']
    sort_list = ['followers', 'repositories', 'joined']
    for order in order_list:
        for sort in sort_list:
            advanced_search(name, page, order, sort)

def advanced_search(name,page,order,sort):
    '''

    :param name:
    :param page:
    :param order:
    :param sort:
    :return:
    '''
    url = "https://api.github.com/search/users?q="+str(name)+"&page="+str(page)+"&per_page=100&sort="+str(sort)+"&order="
    +str(order)
    payload={}
    headers = {
      'Accept': 'application/vnd.github+json',
      'Authorization': 'Bearer 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',
      'X-GitHub-Api-Version': '2022-11-28',
      'Cookie': 'logged_in=no'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except:
        time.sleep(60)
        advanced_search(name,page,order,sort)
    str_response=response.text
    dict_response=json.loads(str_response)
    if page==11:#if arrive to page 11(from page11 not working)
        return None
    else:
        for value in dict_response['items']:
            insert_users_dict(dict_response['items'],dict_response['items'].index(value),1)
            insert_users_dict(name_dict['items'],name_dict['items'].index(value),0)
        advanced_search(name,page+1,order,sort)

def create_db_git_users():
    '''

    :return:
    '''
    list_names=extract_names_from_excel_file()
    for name_ in list_names:
        basic_search(name_, 1)
