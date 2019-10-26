import requests
import random
import time
import sys
import zipfile
from urllib.request import urlretrieve
import pandas as pd
import numpy as  np
from matplotlib import pyplot as plt
from tqdm import tqdm_notebook as tqdm
import geopandas as gpd

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

def get_Moscow_data():
    urlretrieve('http://gis-lab.info/data/mos-adm/ao-shape.zip',\
            filename='/tmp/Moscow.zip', reporthook = reporthook)
    with zipfile.ZipFile('/tmp/Moscow.zip', 'r') as zip_ref:
        zip_ref.extractall('/tmp/Moscow')
    modata = gpd.read_file('/tmp/Moscow/ao.shp')
    return modata


def plot_for_Moscow(dots, modata):
	xs, ys = zip(*dots)
	modata.plot(column = 'ABBREV', linewidth=0.5, cmap='plasma', legend=True, figsize=[15,15])
	plt.scatter(xs, ys, c = 'red')


def get_random_dots(num = 1):
    xs, ys = [], []
    xs = np.random.normal(37.620393, .09, num)
    ys = np.random.normal(55.753960, .05, num)
    return list(zip(xs, ys))# lat, lon


def get_transactions(history_dots, SERVICE = 'https://places.api.here.com/places/v1/discover/explore'):
    transactions = []
    for x, y in tqdm(history_dots, desc = 'get_transactions: '):
        params = {
        'at': str(y)+','+str(x),
        'app_id': 'e2Oc8LGOHx35259d0Glf',
        'app_code': '7k1qMDQtFGum5E8o4GJKGg'
        }
        response = requests.get(SERVICE, params=params)
        transactions.append(response.json())
    return transactions


def get_row(transaction, time, isplace, cols):
    '''
    cols: 'Longtitude', 'Latitude', 'DateTime', 'PlaceCategory', 'OrganizationName',
          'averageRating', 'vicinity', 'openingHours', 'tags', 'PlaceCategoryQuery'
    '''
    res = []
    len_ = len(transaction['results']['items'])
    item = None
    loc = transaction['search']['context']['location']['position']
    if len_ > 0 and isplace:
        i = np.random.choice(np.arange(len_))
        item = transaction['results']['items'][i]
    for col in cols:
#         print(transaction)
        try:
            if col == 'Longtitude':
                res.append(loc[1])
            if col == 'Latitude':
                res.append(loc[0])
            if col == 'DateTime':
                res.append(time)
            if col == 'PlaceCategory':
                    res.append(item['category'] if not(item is None) else None)
            if col == 'OrganizationName':            
                res.append(item['title'] if not(item is None) else None)
            if col == 'averageRating':
                res.append(item['averageRating'] if not(item is None) else None)
            if col == 'vicinity':
                res.append(item['vicinity'] if not(item is None) else 'Moskva')
            if col == 'openingHours':
                res.append(item['openingHours']['text'] if not(item is None) else None)
            if col == 'tags':
                res.append(item['tags'] if not(item is None) else None)
            if col == 'PlaceCategoryQuery':
                cat_l = ['eat-drink', 'restaurant', 'coffee-tea', 'snacks-fast-food', 'going-out',\
                'sights-museums', 'transport', 'airport', 'accommodation', 'shopping', 'leisure-outdoor',\
                'administrative-areas-buildings', 'natural-geographical', 'petrol-station', 'atm-bank-exchange',\
                'toilet-rest-area', 'hospital-health-care-facility']
                cat = np.random.choice(cat_l)
                res.append(cat)
        except Exception as e:
            print(f'Exception happened with {col}: {e}')
            res.append(None)
    return res


def get_random_history(number, UserLocationData_fnm = None, UserQueryData_fnm= None, random_seed = 42):
    if not (random_seed is None):
        random.seed(random_seed)
    dots = get_random_dots(number)
    places_number = int(number*0.7)
    isplaces = [True for _ in range(places_number)] + [False for _ in range(number - places_number)]
    np.random.shuffle(isplaces)
    times = pd.date_range('2018-10-26', '2019-10-26', periods=number)
    transactions = get_transactions(dots)
    UserLocationData_cols = ['Longtitude', 'Latitude', 'DateTime', 'PlaceCategory',\
                             'OrganizationName', 'averageRating',\
            'vicinity', 'openingHours', 'tags']
    UserQueryData_cols = ['DateTime', 'PlaceCategoryQuery']
    table1, table2 = [], []
    for transaction, time, isplace in tqdm(zip(transactions, times, isplaces), desc = 'get_random_history'):
        table1.append(get_row(transaction, time, isplace, UserLocationData_cols))
        table2.append(get_row(transaction, time, True, UserQueryData_cols))
        
    table1 = pd.DataFrame(table1, columns = UserLocationData_cols)
    table2 = pd.DataFrame(table2, columns = UserQueryData_cols)
    if not UserLocationData_fnm is None:
    	table1.to_csv(UserLocationData_fnm+'.csv', index = False)
    if not UserQueryData_fnm is None:
    	table2.to_csv(UserQueryData_fnm+'.csv', index = False)
    return table1, table2
