from typing import Dict, List
import json
import os

import logging
import falcon.media

from recsys.predictor import Predictor


logger = logging.getLogger(__name__)


INTENT_IDS_ENV = 'INTENT_IDS'


class PredictorResource:
    def __init__(self,
                 predictor: Predictor) -> None:
        self.__predictor = predictor

    def __predict(self,
                  latitude: float,
                  longitude: float,
                  n_recommendations: int = 3) -> List[Dict[str, str]]:
        prediction = self.__predictor.predict(latitude=latitude,
                                              longitude=longitude,
                                              n_recommendations=n_recommendations)
        if prediction:
            return prediction
        return []

    def on_get(self, request: falcon.Request, response: falcon.Response):
        latitude = request.get_param_as_float('latitude', required=True)
        longitude = request.get_param_as_float('longitude', required=True)
        n_recommendations = request.get_param_as_int('n', required=False)
        logger.info(f'Received request: latitude={latitude} longitude={longitude}')

        response.media = self.__predict(latitude=latitude,
                                        longitude=longitude,
                                        n_recommendations=n_recommendations)
        logger.info(f'Response send: {response.media}')


def get_app() -> falcon.API:
    logger.info('Starting recsys...')

    predictor = Predictor()

    app = falcon.API()
    app.add_route('/get_recommendation', PredictorResource(predictor=predictor))

    # treat commas as literal characters here
    # https://falcon.readthedocs.io/en/stable/api/api.html#falcon.RequestOptions.auto_parse_qs_csv
    app.req_options.auto_parse_qs_csv = False
    return app
