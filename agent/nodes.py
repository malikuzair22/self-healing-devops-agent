import uuid
from agent.state import AgentState
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json
import os
from tools.k8s_tool import restart_pod
from tools.github_tool import create_issue
from api.database import save_incidents

load_dotenv()
model = ChatGroq(model="llama-3.3-70b-versatile")

def observe_node(state: AgentState) -> dict:
    logs = state['logs']
    metrics = state['metrics']
    return {
        'logs': logs,
        'metrics': metrics,
        'incident_id': str(uuid.uuid4()),
        'source': 'pod'
    }
    
def diagnose_node(state: AgentState) -> dict:
    logs = state['logs']
    metrics = state['metrics']

    SystemPrompt = """You are an expert SRE. Analyze the logs and metrics.
                 You MUST respond with ONLY a valid JSON object, no extra text, no markdown, no backticks.
                 Example: {"diagnosis": "Memory exhaustion", "confidence": 0.9}"""
    UserPrompt = f"Logs: {logs}\nMetrics: {metrics}"
   

    response = model.invoke([
        SystemMessage(content= SystemPrompt),
        HumanMessage(content= UserPrompt)
    ])

    try:
        content = response.content.strip()
        # Remove markdown backticks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {"diagnosis": "Unable to parse diagnosis", "confidence": 0.5}
    return {
    'diagnosis': result['diagnosis'],
    'confidence': result['confidence']
    }

def decide_node(state: AgentState)  -> dict:
    confidence = state['confidence']
    if confidence >= float(os.getenv('CONFIDENCE_THRESHOLD')):
        return {'status': 'auto-fix'}
    else:
        return {'status': 'manual-review'}
    

    
def act_node(state: AgentState) -> dict:
    status = state['status']
    if status == "auto-fix":
        result = restart_pod(state['pod_name'])
        return {'action_taken': 'pod-restart'}
    else:
        result = create_issue(
            state['diagnosis'],
            state['confidence'],
            state['logs']
        )
        return {'action_taken': 'github-issue_created'}

def verify_node(state: AgentState)-> dict:
    action_taken = state['action_taken']
    if action_taken == 'pod-restart':
        print("Verifying pod restart...")
        # Implement verification logic here
        return {'status': 'auto-resolved'}
    else:
        print("Verifying manual review...")
        # Implement verification logic here
        return {'status': 'escalated'}
    

def log_node(state: AgentState) -> dict:
    incident_id = state['incident_id']
    diagnosis = state['diagnosis']
    source = state['source']
    action_taken = state['action_taken']
    confidence = state['confidence']
    status = state['status']

    incident= {
        'incident_id': incident_id,
        'source': source,
        'diagnosis': diagnosis,
        'confidence': confidence,
        'action_taken': action_taken,
        'final_status': status
    }
    save_incidents({
    'incident_id': incident_id,
    'source': source,
    'diagnosis': diagnosis,
    'confidence': confidence,
    'action_taken': action_taken,
    'status': status
    })
    print(f"Logging incident: {json.dumps(incident, indent=2)}")
    # Implement logging logic here (e.g., write to a database or file)
    return {}