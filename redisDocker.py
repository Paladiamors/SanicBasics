import docker

client = docker.from_env()

name = "redis_test"
ports = {"6379/tcp": "6379"}
image = "redis:latest"


def start_container():
    container = client.containers.list(all=True, filters={"name": name})
    if container and container[0].status == "exited":
        print("starting container")
        container = container[0]
        container.start()

    elif not container:
        print("running container")
        client.containers.run(image, ports=ports, name=name, detach=True)
    elif container and container[0].status == "running":
        print("this container is still running")
    else:
        print("state of container is unknown")


def stop_container():
    container = client.containers.list(filters={"name": name})
    if container:
        print("stopping container")
        container[0].stop()
    else:
        print("the container was not running")


def clean_containers():
    """
    deletes all the containers
    that are stopped
    """

    containers = client.containers.list(all=True, filters={"status": "exited"})
    for container in containers:
        print("cleaning container", container.name, container.image)
        container.remove()


def clean_container():
    """
    deletes a container by name
    """

    containers = client.containers.list(all=True, filters={"name": name})
    if containers:
        print("removing container")
        containers[0].remove()
    else:
        print("no container to remove")


if __name__ == '__main__':
    
    # TODO: Add an argparser here
    #     start_container()
    #     clean_containers()

    #     stop_container()
    start_container()
#     stop_container()
#     clean_container()
