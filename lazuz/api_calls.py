import csv
from datetime import datetime
import requests
from typing import Optional
from pathlib import Path
from functools import partial

import yaml


CONFIG_FILE = Path("configs/api_calls.yaml")


def read_http_headers_file(filepath: Path) -> dict:
    with open(filepath, mode="r") as file:
        reader = csv.reader(file)

        return {row[0]: row[1] for row in reader}


class ApiCall:
    def __init__(
        self,
        url: str,
        method: str,
        headers: Path,
        body: Optional[Path] = None,
        query: Optional[Path] = None,
        token: Optional[str] = None,
    ):
        self.url = url
        self.method = method
        self._headers = read_http_headers_file(headers)

        self.body = read_http_headers_file(body) if body else None
        self.query = read_http_headers_file(query) if query else None
        self.token = token

    @property
    def headers(self):
        if self.token:
            self._headers["Authorization"] = f"Bearer {self.token}"
        return self._headers

    @property
    def request(self):
        method = requests.post if self.method == "POST" else requests.get
        return partial(
            method, self.url, headers=self.headers, data=self.body, params=self.query
        )


class ApiCalls:
    def __init__(self):
        with open(CONFIG_FILE, "r") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

        self.token = None
        self.generate_authentication_token()

    def __getitem__(self, key: str) -> ApiCall:
        return ApiCall(**self.config[key], token=self.token)

    def generate_authentication_token(self) -> None:
        response = self["authentication"].request()
        self.token = response.json()["result"]["accessToken"]

    def available_slots(self, club_id: int) -> dict:
        response = self["available_slots"].request()
        return response

    def clubs_by_id(self, club_id: int, date: datetime) -> dict:
        request = self["clubs_by_id"]
        request.query["clubIds"] = [str(club_id)]
        request.query["date"] = date.strftime("%Y-%m-%d")

        return request.request()

    def clubs_by_multiple_id(self, club_ids: list[int], date: datetime) -> dict:
        request = self["clubs_by_id"]
        request.query["clubIds"] = ",".join(str(id) for id in club_ids)
        request.query["date"] = date.strftime("%Y-%m-%d")

        return request.request()
