# %%
from kubernetes.client import V1PodTemplateSpec
from kubernetes.client import V1ObjectMeta
from kubernetes.client import V1PodSpec
from kubernetes.client import V1Container

from kubeflow.training.utils import utils
from kubeflow.training import V1ReplicaSpec
from kubeflow.training import V1RunPolicy
from kubeflow.training import V1TFJob
from kubeflow.training import V1TFJobSpec
from kubeflow.training import TFJobClient

# %%
namespace = utils.get_default_target_namespace()

container = V1Container(
    name="tensorflow",
    image="horovod/horovod:latest",
    command=[
        "horovodrun",
        "-np", "2",
        "-H", "localhost:2",
        "python", "./tensorflow2/tensorflow2_mnist.py"
    ],
    resources={
        "limits": {
            "nvidia.com/gpu": "2",
            "memory": "2Gi"
        }
    },
    env=[
        {
            "name": "NVIDIA_VISIBLE_DEVICES",
            "value": "0,1"
        }
    ]
)

chief = V1ReplicaSpec(
    replicas=1,
    restart_policy="Never",
    template=V1PodTemplateSpec(
        spec=V1PodSpec(
            containers=[container],
        )
    )
)

ps = V1ReplicaSpec(
    replicas=1,
    restart_policy="Never",
    template=V1PodTemplateSpec(
        spec=V1PodSpec(
            containers=[container],
        )
    )
)

tfjob = V1TFJob(
    api_version="kubeflow.org/v1",
    kind="TFJob",
    metadata=V1ObjectMeta(name="mnist",namespace=namespace),
    spec=V1TFJobSpec(
        run_policy=V1RunPolicy(clean_pod_policy="None"),
        tf_replica_specs={
            "Chief": chief,
            "PS": ps
        }
    )
)

tfjob_client = TFJobClient()
tfjob_client.create(tfjob, namespace=namespace)

# %%
tfjob_client.get('mnist', namespace=namespace)

# %%
tfjob_client.get_job_status('mnist', namespace=namespace)

# %%
tfjob_client.is_job_succeeded('mnist', namespace=namespace)

# %%
tfjob_client.delete('mnist', namespace=namespace)