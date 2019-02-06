import docker
import io
import os


class BaseImage(object):
    def __init__(self, name, package, py_version):
        self.cur_path = os.path.abspath(os.path.curdir)
        self.name = name
        self.package = package
        self.py_version = py_version
        self.docker_file = io.BytesIO()

    def generate_docker_file(self):
        self.docker_file.write(f"FROM python:{self.py_version} \n".encode("utf-8"))
        self.docker_file.write(f"ADD . /{self.package.name} \n".encode("utf-8"))
        self.docker_file.write(f"WORKDIR /{self.package.name} \n".encode("utf-8"))
        self.docker_file.write("RUN pwd \n".encode("utf-8"))
        self.docker_file.write("RUN ls -l \n".encode("utf-8"))
        if self.package.requirements:
            self.docker_file.write(f"RUN pip{self.py_version} install -r requirements.txt\n".encode("utf-8"))
        self.docker_file.write(f"CMD python{self.py_version} consumer.py".encode("utf-8"))

    def build_image(self, host_url="unix://var/run/docker.sock"):
        client = docker.DockerClient(host_url)
        try:
            os.chdir(self.package.path)
            client.images.build(fileobj=self.docker_file, tag=self.name, nocache=True)
        except Exception as e:
            print(f"failed to build using fileobj due to {str(e)}")
            print("attempting to build using on-disk dockerfile")
            os.system(f"touch {self.package.path}/Dockerfile")
            os.system(f'echo "{self.docker_file.getvalue().decode("utf-8")}" > {self.package.path}/Dockerfile')
            client.images.build(path=self.package.path, tag=self.name, nocache=True)

    def __del__(self):
        os.chdir(self.cur_path)



class BaseContainer(object):
    def __init__(self, name, image, host_url="unix://var/run/docker.sock"):
        self.client = docker.DockerClient(host_url)
        self.name = name
        if isinstance(image, str):
            self.image = image
        elif isinstance(image, BaseImage):
            self.image = image.name
        else:
            if hasattr(image, "name"):
                self.image = image.name
            else:
                raise TypeError(f"expecting string or BaseImage object but got {type(image)} instead")

    def run(self, environment, **kwargs):
        self.client.containers.run(image=self.image, environment=environment, detach=True, **kwargs)

