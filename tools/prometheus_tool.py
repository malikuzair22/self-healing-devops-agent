
import requests


def query_prometheus(query:str)-> dict:
    try:
        # Replace with your Prometheus server URL
        prometheus_url = "http://localhost:9091/api/v1/query"
        response = requests.get(prometheus_url, params={"query": query})
        data = response.json()
        result = data['data']['result']
        if not result:
            return {"success": False, "message": "No data found for the given query"}
        value = float(result[0]['value'][1])  # Extract the value from the result
        return {"success": True, "value": value}
    except Exception as e:
        return {"success": False, "message": str(e)}