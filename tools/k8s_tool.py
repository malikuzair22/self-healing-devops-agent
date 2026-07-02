from kubernetes import client, config

def restart_pod(pod_name: str) -> dict:
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        v1.delete_namespaced_pod(name=pod_name, namespace="default")
        return {"success": True, "message": f"Pod {pod_name} restarted"}
    except Exception as e:
        return {"success": False, "message": str(e)}