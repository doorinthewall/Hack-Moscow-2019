from typing import Dict, List, Optional

import requests
import pandas as pd
import logging

from recsys.history.loader import HistoryLoader
from recsys.history import REQUESTS_PATH, LOCATIONS_PATH


logger = logging.getLogger(__name__)


class UserFilter:
    def __init__(
        self,
        user_id: str = '',
        location_history: pd.DataFrame = None,
        request_history: pd.DataFrame = None
    ):
        self.__user_id = user_id
        self.location_history = location_history
        self.request_history = request_history

    def make_frequency_cat_filter(self):
        res = []
        if 'PlaceCategory' in self.location_history.columns:
            res += list(self.location_history['PlaceCategory'].mode().values)
        if 'PlaceCategoryQuery' in self.request_history.columns:
            res += list(self.request_history['PlaceCategoryQuery'].mode().values)
        res = list(filter(lambda x: x != '', res))
        return res

    def get_cat_filters(self):
        return self.make_frequency_cat_filter()
    
    def get_rating_filter(self, cat_filters):
        mean_rating = 0.
        if 'averageRating' in self.location_history.columns:
            if len(cat_filters) > 0:
                mean_rating = self.location_history[self.location_history['PlaceCategory'].isin(cat_filters)]['averageRating'].mean()
            else:
                mean_rating = self.location_history['averageRating'].mean()
        
        def filt(item):
            if 'averageRating' in item:
                return item['averageRating'] >= mean_rating
            return True
        return filt

    def get_other_filters(self, cat_filters):
        return [self.get_rating_filter(cat_filters)]


class Predictor:
    def __init__(
        self,
        user_id: str = '',
        user_password: str = ''
    ):
        self.__user_id = user_id
        self.__user_password = user_password
        self.__requests_loader = HistoryLoader(REQUESTS_PATH)
        self.__locations_loader = HistoryLoader(LOCATIONS_PATH)

    def check_cat(self, cat):
        valid_cats = set([
            'eat-drink',
            'restaurant',
            'coffee-tea',
            'snacks-fast-food',
            'going-out',
            'sights-museums',
            'transport',
            'airport',
            'accommodation',
            'shopping',
            'leisure-outdoor',
            'administrative-areas-buildings',
            'natural-geographical',
            'petrol-station',
            'atm-bank-exchange',
            'toilet-rest-area',
            'hospital-health-care-facility'
        ])
        return cat in valid_cats
    
    def predict(self,
                latitude: float,
                longitude: float,
                n_recommendations: int = 3,
                cat_filters: Optional[List[str]] = None,
                other_filters: Optional[List[str]] = None,
                location_history: pd.DataFrame = None,
                request_history: pd.DataFrame = None
               ) -> Optional[List[Dict[str, str]]]:
        checkpoint = {
            'Longtitude': longitude,
            'Latitude': latitude,
            'PlaceCategory': ','.join(cat_filters) if cat_filters else ''
        }
        self.__locations_loader.save(checkpoint)
        checkpoint = {
            'PlaceCategoryQuery': ','.join(cat_filters) if cat_filters else '',
        }
        self.__requests_loader.save(checkpoint)

        APP_ID = 'e2Oc8LGOHx35259d0Glf'
        APP_CODE = '7k1qMDQtFGum5E8o4GJKGg'

        if n_recommendations >= 99:
            n_recommendations = 99
        at = str(latitude) + ',' + str(longitude)
        
        # filters that can be processed inside of the request
        location_history = self.__locations_loader.load()
        request_history = self.__requests_loader.load()
        user_filter = UserFilter(self.__user_id, location_history, request_history)
        new_cat_filters = []
        if cat_filters:
            for cat in cat_filters:
                if self.check_cat(cat):
                    new_cat_filters.append(cat)
            cat_filters = new_cat_filters
        else:
            cat_filters = user_filter.get_cat_filters()
        
        params = {
            'at': at,
            'app_id': APP_ID,
            'app_code': APP_CODE,
            'size': str(n_recommendations)
        }
        if len(cat_filters) != 0:
            logger.info(f'{cat_filters}')
            params['cat'] = ','.join(cat_filters)
        
        response = requests.get(
            'https://places.api.here.com/places/v1/discover/explore',
            params=params
        ).json()
        
        # other filters
        if other_filters:
            other_filters = user_filter.get_other_filters(cat_filters) + other_filters
        else:
            other_filters = user_filter.get_other_filters(cat_filters)

        result = self.process_response(response, other_filters)
        if n_recommendations > 0:
            return result
        return None
    
    def process_fields_with_br(self, text):
        if text == 'unknown':
            return text
        res_text = ', '.join(text.split('<br/>'))
        return res_text
        
    def process_response(self, response, filters):
        if 'results' not in response or 'items' not in response['results'] or len(response['results']['items']) == 0:
            return None

        items = response['results']['items']

        filtered_items = self.filter_items(items, filters)
        result = [{
            'name': item.get('title', 'unknown'),
            'address': self.process_fields_with_br(
             item.get('vicinity', 'unknown')),
            'open': self.process_fields_with_br(
             item.get('openingHours', {'text': 'unknown'}).get('text', 'unknown')
            )
        } for item in filtered_items]

        return result
    
    def filter_items(self, items, filters):
        res = []
        
        for item in items:
            add = True
            for f in filters:
                if not f(item):
                    add = False
                    break
            if add:
                res.append(item)
        return res
