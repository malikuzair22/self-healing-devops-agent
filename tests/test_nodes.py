from agent.nodes import decide_node, act_node, verify_node
from unittest.mock import patch

def test_decide_node_high_confidence():
    state = {
        "confidence": 0.9}
    result = decide_node(state)
    assert result['status'] == 'auto-fix'

def test_decide_node_low_confidence():
    state = {"confidence": 0.3}
    result = decide_node(state)
    assert result['status'] == 'manual-review'

@patch('agent.nodes.restart_pod')
def test_act_node_auto_fix(mock_restart_pod):
    mock_restart_pod.return_value = {"success": True, "message": "pod restart"}
    
    state = {"status": "auto-fix", "pod_name": "test-pod"}
    result = act_node(state)

    assert result['action_taken'] == 'pod-restart'
    mock_restart_pod.assert_called_once()


def test_verify_node_pod_restart():
    state = {"action_taken": "pod-restart"}
    result = verify_node(state)
    assert result['status'] == 'auto-resolved'

def test_verify_node_escalated():
    state = {"action_taken": "github-issue_created"}
    result = verify_node(state)
    assert result['status'] == 'escalated'

    
    
