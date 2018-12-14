import pika
import importlib
import json
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


def getFile(package, name):
    if package:
        return importlib.import_module(f'{package}.{name}')
    else:
        return importlib.import_module(name)

def getFunction(file, name):
    return getattr(file, name)


def send_message(queue, result):
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue)
    ch.basic_publish(exchange='', routing_key=queue, body=result)
    ch.close()


def consumerFunction(ch, method, props, body):
        jbody = json.loads(body.decode("utf-8"))
        args = jbody.get('args', [])
        kwargs = jbody.get('kwargs', {})
        return_queue = jbody.pop('return_queue')
        mod = getFile(None, 'function')
        func = getFunction(mod, os.environ.get("FUNCTION_NAME"))
        try:
            res = func(*args, **kwargs)
            send_message(return_queue, json.dumps({'succeed': True, 'result': res}))
        except Exception as e:
            send_message(return_queue, json.dumps({'succeed': False, 'exception': str(e)}))
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    while True:
        try:
            ch.queue_declare(os.environ.get('FUNCTION_QUEUE'))
            ch.basic_consume(consumerFunction, no_ack=False, queue=os.environ.get('FUNCTION_QUEUE'))
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