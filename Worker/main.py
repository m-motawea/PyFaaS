#!/bin/python3.6
import pika
import json
from utils.package_util import FaaSPackage
from utils.docker_utils import BaseImage, BaseContainer
import os


creds = pika.PlainCredentials(
        username=os.environ.get("BROKER_USERNAME"),
        password=os.environ.get("BROKER_PASSWORD")
    )
params = pika.ConnectionParameters(
        host=os.environ.get("BROKER_ADDRESS"),
        port=os.environ.get("BROKER_PORT"),
        credentials=creds
    )


def consumer(ch, method, props, body):
    try:
        jbody = json.loads(body)
        p = FaaSPackage(
            name=jbody["function"],
            uuid=jbody["uuid"],
            code=jbody["code"],
            requirements=jbody["requirements"],
            py_version=jbody["version"],
            functions_path=os.environ.get("FUNCTIONS_PATH"),
            broker_address=os.environ.get("F_BROKER_ADDRESS"),
            broker_port=os.environ.get("F_BROKER_PORT"),
            broker_username=os.environ.get("F_BROKER_USERNAME"),
            broker_password=os.environ.get("F_BROKER_PASSWORD")
        )
        p.generate_code()
        p.generate_env_dict()

        img = BaseImage(
            name=p.uuid,
            package=p,
            py_version=p.version
        )
        img.generate_docker_file()
        img.build_image()

        cnt = BaseContainer(
            name=p.uuid,
            image=img
        )
        cnt.run(p.env_dict)
    except Exception as e:
        print(f"exception while building image {str(e)}")
        return
    ch.basic_ack(delivery_tag=method.delivery_tag)



def main():
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    while True:
        try:
            ch.queue_declare("faas")
            ch.basic_consume(consumer, no_ack=False, queue="faas")
            ch.start_consuming()
        except Exception as e:
            print(f"exception: {str(e)}")
            try:
                conn.close()
                ch.close()
            except Exception as e:
                print(f"exception closing connection {str(e)}")
            conn = pika.BlockingConnection(params)
            ch = conn.channel()

if __name__ == "__main__":
    main()