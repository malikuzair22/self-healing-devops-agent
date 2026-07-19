from tools.k8s_tool import scale_deployment, restart_pod

import os
import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Integration tests require a real Minikube cluster, not available in CI"
)


def test_scale_deployment_integration():
    result = scale_deployment('target-app', 3)

    assert result['success'] == True

    scale_deployment('target-app', 2)

def test_restart_pod_integration():
    result = restart_pod('target-app-867d9c8996-6gb46')

    assert result['success'] == True

    

