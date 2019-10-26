from typing import Dict, List, Optional


class Predictor:
    def __init__(self, user_id: str = '', user_password: str = ''):
        self.__user_id = user_id
        self.__user_password = user_password

    def predict(self,
                latitude: float,
                longitude: float,
                n_recommendations: int = 3) -> Optional[List[Dict[str, str]]]:
        result = [{
            'name': 'Bar Some team',
            'address': 'MSU',
            'open': '9:30-22:00'
        }]
        if n_recommendations > 0:
            return result
        return None
