import config

def get_docker_client(server: str):
    if server == "gpu3":
        return config.GPU3_DOCKER_CLIENT
    elif server == "gpu4":
        return config.GPU4_DOCKER_CLIENT
    elif server == "gpu5":
        return config.GPU5_DOCKER_CLIENT