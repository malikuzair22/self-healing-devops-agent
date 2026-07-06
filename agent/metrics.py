from prometheus_client import Histogram, Counter, start_http_server

incident_total = Counter('agent_incident_total', 'Total incidents processed by the agent', ['status'])

diagnosis_histogram = Histogram('agent_diagnosis_confidence','Confidence levels of diagnoses made by the agent', buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) 

def start_metrics_server(port: int = 8001):
    """
    Starts the Prometheus metrics server on the specified port.
    """
    start_http_server(port)
    print(f"Metrics server started on port {port}")
    
