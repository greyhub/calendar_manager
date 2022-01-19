import json
import logging
from pprint import pprint

import requests
from json.decoder import JSONDecodeError
from response import success, ApiBadRequest, ApiInternalError
from config import ExternalAPI
from services import convert_class_time_table


class RouteHandler:

    async def get_time_table(self, request):
        body = await decode_request(request)
        request_data = json.dumps(body)
        time_table = requests.post(ExternalAPI.url, data=request_data, headers={'Content-Type': "application/json"})
        class_schedule = convert_class_time_table(time_table.json())
        response = class_schedule
        return success(response)

    async def get_activities(self, request):
        body = await decode_request(request)
        try:
            write_graph = request.rel_url.query['write_graph']
        except Exception as e:
            raise ApiBadRequest(
                "Make sure that you are sending enough parameter: write_graph")


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')
