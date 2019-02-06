import pika
import base64
import json
import uuid
import datetime

class SimpleClient():
    def __init__(self, host, port, username, password, vhost):
        creds = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(
            credentials=creds,
            host=host,
            port=port,
            virtual_host=vhost
        )
        self.conn = pika.BlockingConnection(parameters=params)
        self.ch = self.conn.channel()

    def create_queue(self, name):
        self.ch.queue_declare(name)

    def delete_queue(self, name):
        self.ch.queue_delete(name)

    def send(self, queue, message, exchange=''):
        self.ch.basic_publish(
            exchange=exchange,
            routing_key=queue,
            body=message
        )

    def listen(self, queue, exchange="", timeout=30, callback=None):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        if not callback:
            while True:
                if datetime.datetime.now() < end_time:
                    method_frame, header_frame, body = self.ch.basic_get(queue=queue)
                    if method_frame.NAME != 'Basic.GetEmpty':
                        self.ch.basic_ack(delivery_tag=method_frame.delivery_tag)
                        return body
                else:
                    raise TimeoutError(f"no message received in period: {timeout} seconds")
        else:
            self.ch.basic_consume(callback, queue=queue, exchange="", no_ack=False)
            self.ch.start_consuming()


    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            pass

    
class FaaSClient(SimpleClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_queue('faas')
    

    def create_function(self, name, code_file, requirements_file, version, queue='faas', exchange=''):
        function_uuid = uuid.uuid4().hex
        code_64_encoded_str = base64.encodebytes(code_file).decode('utf-8')
        requirements_64_encoded_str = base64.encodebytes(requirements_file).decode('utf-8')
        body = {
            'uuid': function_uuid,
            'function': name,
            'code': code_64_encoded_str,
            'requirements': requirements_64_encoded_str,
            'version': version
        }
        self.send(queue, json.dumps(body), exchange)
        return function_uuid


    def call_blocking_function(self, func_uuid, body, faas_consumers_queue="faas_listeners"):
        return_queue = uuid.uuid4().hex
        body["return_queue"] = return_queue
        self.send(func_uuid, json.dumps(body), "")
        result = self.listen(return_queue)
        if result:
            self.delete_queue(return_queue)
            return json.loads(result)



    def call_async_function(self, func_uuid, body, faas_consumers_queue="faas_listeners"):
        return_queue = uuid.uuid4().hex
        body["return_queue"] = return_queue
        listener_body = {
            "uuid": func_uuid,
            "return_queue": return_queue,
            "type": "function",
            "async": True
        }
        self.send(faas_consumers_queue, json.dumps(listener_body), "")
        self.send(func_uuid, json.dumps(body), "")