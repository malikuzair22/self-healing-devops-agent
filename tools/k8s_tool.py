from kubernetes import client, config
import subprocess


def restart_pod(pod_name: str) -> dict:
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        v1.delete_namespaced_pod(name=pod_name, namespace="default")
        return {"success": True, "message": f"Pod {pod_name} restarted"}
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def scale_deployment(deployment_name: str, replicas: int, namespace: str = "default") -> dict:
    try:
        config.load_kube_config()
        apps_v1 = client.AppsV1Api()
        body = {"spec": {"replicas": replicas}}
        apps_v1.patch_namespaced_deployment_scale(name=deployment_name, namespace=namespace, body=body)
        return {"success": True, "message": f"Deployment {deployment_name} scaled to {replicas} replicas"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def rollback_deployment(deployment_name: str, namespace: str = "default") -> dict:
    try:
        config.load_kube_config()
        # Use kubectl command to rollback deployment
        subprocess.run(["kubectl", "rollout", "undo", f"deployment/{deployment_name}", "-n", namespace], check=True, capture_output=True, text=True)
        return {"success": True, "message": f"Deployment {deployment_name} rolled back"}
    except Exception as e:
        return {"success": False, "message": str(e)}