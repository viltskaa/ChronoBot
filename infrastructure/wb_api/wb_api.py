from infrastructure.wb_api.base import BaseClient
from datetime import datetime
import requests


class WBApi(BaseClient):

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://discounts-prices-api.wildberries.ru"
        self.analytics_url = "https://seller-analytics-api.wildberries.ru"
        super().__init__(base_url=self.base_url)

    async def get_goods(self, limit_goods=1000, offset_goods=0, filter_nm_id=None):
        endpoint = "/api/v2/list/goods/filter"
        headers = {
            'Authorization': f'{self.api_key}'
        }
        params = {
            'limit': limit_goods,
            'offset': offset_goods
        }

        if filter_nm_id is not None:
            params['filterNmID'] = filter_nm_id

        self.log.info(
            "Making GET request to %s with params: %s and headers: %s",
            self.base_url + endpoint,
            params,
            headers
        )

        try:
            status, data = await self._make_request(
                method="GET",
                url=endpoint,
                params=params,
                headers=headers
            )

            self.log.info(
                "Received response from %s with status %d and data: %s",
                self.base_url + endpoint,
                status,
                data
            )

            return data
        except Exception as e:
            self.log.error(f"An error occurred during request: {e}", exc_info=True)
            raise

    async def get_nm_report(self, ids: list[int]):
        self.set_url(self.analytics_url)
        endpoint = "/api/v2/nm-report/detail/history"
        headers = {
            'Authorization': f'{self.api_key}'
        }

        json = {
            'nmIDs': ids,
            'period': {
                'begin': "2024-07-03",
                'end': "2024-07-03"
            }
        }

        response = requests.post(
            self.analytics_url + endpoint,
            headers=headers,
            json=json
        )

        print(response.status_code)
        return response.json()


        # try:
        #     status, data = await self._make_request(
        #         method="POST",
        #         url=endpoint,
        #         json=json,
        #         headers=headers
        #     )
        #
        #     self.log.info(
        #         "Received response from %s with status %d and data: %s",
        #         self.base_url + endpoint,
        #         status,
        #         data
        #     )
        #
        #     return data
        # except Exception as e:
        #     self.log.error(f"An error occurred during request: {e}", exc_info=True)
        #     raise

