from kubernetes import client, config

def update_deployment(deployment, release, namespace, **kwargs):
    # Loads the Kubernetes config from default location
    config.load_kube_config()
    # Calls Kubernetes API
    api = client.AppsV1Api()
    #Reads the specified deployment
    # Calls function to update data
    for (deployment, release) in zip(deployment, release):
        deployment_object = api.read_namespaced_deployment(name=deployment, namespace=namespace)
        # Update container image
        old_data = deployment_object.spec.template.spec.containers[0].image
        deployment_object.spec.template.spec.containers[0].image = f"974112515744.dkr.ecr.us-east-1.amazonaws.com/{release}"
        print(old_data)
        resp = api.patch_namespaced_deployment(
            name = deployment,
            namespace= namespace,
            body= deployment_object
        )
        #print(old_data)
        print("\n[INFO] deployment's container image updated.\n")
        print("NAMESPACE", "NAME", "REVISION", "IMAGE")
        print(f"{resp.metadata.namespace}, {resp.metadata.name}, {resp.metadata.generation}, {resp.spec.template.spec.containers[0].image}")
