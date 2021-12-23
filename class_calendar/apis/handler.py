import json
import requests
from json.decoder import JSONDecodeError
from response import success, ApiBadRequest, ApiInternalError
from config import ExternalAPI


class RouteHandler:

    async def get_time_table(self, request):
        body = await decode_request(request)
        request_data = json.dumps(body)
        time_table = requests.post(ExternalAPI.url, data=request_data, headers={'Content-Type': "application/json"})
        response = time_table.json()
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
