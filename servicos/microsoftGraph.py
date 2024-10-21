import requests

class MicrosoftGraph:
    @staticmethod
    def call_graph_api(token: str):
        try:
            graph_url = 'https://graph.microsoft.com/v1.0/me'
            headers = {'Authorization': token}
            graph_response = requests.get(graph_url, headers=headers)
            if graph_response.status_code != 200:
                return {'message': 'Failed to call Microsoft Graph API', 'error': graph_response.json()}, graph_response.status_code
            return graph_response.json(), 200
        except Exception as e:
            return {'message': f'Token is invalid! Error: {str(e)}'}, 401