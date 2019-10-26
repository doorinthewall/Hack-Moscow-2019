from typing import Dict
import pathlib

import pandas as pd


class HistoryLoader:
    def __init__(self, path: pathlib.Path):
        self.__path = path
        self.__data = pd.read_csv(path)

    def load(self) -> pd.DataFrame:
        return self.__data

    def save(self, checkpoint: Dict[str, str]):
        self.__data = self.__data.append(checkpoint, ignore_index=True)
        self.__data.to_csv(self.__path)
