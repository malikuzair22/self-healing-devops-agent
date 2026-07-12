from unittest.mock import patch
from agent.graph import app
import uuid


@patch('agent.nodes.send_slack_alert')
@patch('agent.nodes.create_issue')
def test_e2e_low_confidence_escalation(mock_create_issue, mock_send_slack):
    mock_create_issue.return_value = {"success": True, "issue_url":"http"}
    mock_send_slack.return_value = {"success": True}

    config = {"configurable": {"thread_id": str(uuid.uuid4())}} 
    result = app.invoke({
        "logs": "Random unknown error",
        "metrics": "cpu_usage: 45%, memory: 60%",
        "pod_name":"test_pod"
    }, config= config)

    assert result['status'] == 'escalated'
    assert result['action_taken'] == 'github-issue_created'
    mock_create_issue.assert_called_once()

@patch('agent.nodes.restart_pod')
@patch('agent.nodes.send_slack_alert')
@patch('agent.nodes.diagnose_node')
def test_e2e_high_confidence_autofix(mock_model, mock_slack, mock_restart):
    fake_response = type('obj', (), {'content': '{"diagnosis": "Memory exhaustion", "confidence": 0.95}'})()
    mock_model.invoke.return_value = fake_response 
    mock_restart.return_value = {"success": True}
    mock_slack.return_value = {"success": True}

    config = {"configurable": {"thread_id": str(uuid.uuid4())}} 
    result = app.invoke({
        "logs": "Need to fixed ",
        "metrics": "cpu_usage: 80%, memory: 75%",
        "pod_name":"test_pod"
    }, config= config)

    assert result['status'] == 'auto-resolved'
    assert result['action_taken'] == 'pod-restart'
    mock_restart.assert_called_once()



