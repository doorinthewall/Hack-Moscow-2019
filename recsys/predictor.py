from typing import Dict, List, Optional
import requests
import pandas as pd


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
        if 'PlaceCategory' in self.location_history.columns():
            res += [self.location_history['PlaceCategory'].mode()]
        if 'PlaceCategoryQuery' in self.request_history.columns():
            res += [self.request_history['PlaceCategoryQuery'].mode()]
        return res

    def get_cat_filters(self):
        return self.make_frequency_cat_filter()
    
    def get_other_filters(self):
        return []
    

class Predictor:
    def __init__(
        self,
        user_id: str = '',
        user_password: str = ''
    ):
        self.__user_id = user_id
        self.__user_password = user_password

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
        APP_ID = 'e2Oc8LGOHx35259d0Glf'
        APP_CODE = '7k1qMDQtFGum5E8o4GJKGg'

        if n_recommendations >= 99:
            n_recommendations = 99
        at = str(latitude) + ',' + str(longitude)
        
        # filters that can be processed inside of the request
        user_filter = UserFilter(self.__user_id, location_history, request_history)
        new_cat_filters = []
        if cat_filters:
            for cat in user_filter.get_cat_filters() + cat_filters:
                if self.check_cat(cat):
                    new_cat_filters.append(cat)
        cat_filters = new_cat_filters
        
        params = {
            'at': at,
            'app_id': APP_ID,
            'app_code': APP_CODE,
            'size': str(n_recommendations)
        }
        if len(cat_filters) != 0:
            params['cat'] = ','.join(cat_filters)
        
        response = requests.get(
            'https://places.api.here.com/places/v1/discover/explore',
            params=params
        ).json()
        
        # other filters
        if other_filters:
            other_filters = self.__user_filter.get_other_filters() + other_filters
        else:
            other_filters = self.__user_filter.get_other_filters()

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
