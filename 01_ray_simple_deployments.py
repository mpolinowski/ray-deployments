import ray
from ray import serve
import requests
from starlette.requests import Request
from uuid import uuid4

# start Ray
ray.init()

# start Serve
serve.start()

#define deployment
@serve.deployment
class Converter:
    def __call__(self, request):
        if request.query_params["conversion"] == 'CF' :
            return {"INFO :: Fahrenheit temperature":
                        9.0/5.0 * float(request.query_params["temp"]) + 32.0}
        elif request.query_params["conversion"] == 'FC' :
            return {"INFO :: Celsius temperature":
                        (float(request.query_params["temp"]) - 32.0) * 5.0/9.0 }
        else:
            return {"ERROR :: Unknown conversion code" : request.query_params["conversion"]}


Converter.deploy()
# list current deployment
print(serve.list_deployments()) 


# query our endpoint over http
print(requests.get("http://127.0.0.1:8000/Converter?temp=999.0&conversion=CF").text)
print(requests.get("http://127.0.0.1:8000/Converter?temp=999.0&conversion=FC").text)
print(requests.get("http://127.0.0.1:8000/Converter?temp=999.0&conversion=CC").text)


# direct invocation
from starlette.requests import Request
handle = serve.get_deployment('Converter').get_handle()

print(ray.get(handle.remote(Request({"type": "http", "query_string": b"temp=666.0&conversion=CF"}))))
print(ray.get(handle.remote(Request({"type": "http", "query_string": b"temp=666.0&conversion=FC"}))))
print(ray.get(handle.remote(Request({"type": "http", "query_string": b"temp=666.0&conversion=CC"}))))


# simplifying the converter
# adding scale factor
@serve.deployment(ray_actor_options={"num_cpus": 1, "num_gpus":0}, route_prefix="/converter/simple", num_replicas=2)
class ConverterSimple:
    # generate instance id
    def __init__ (self):
        self.id = str(uuid4())

    def celcius_fahrenheit(self, temp):
        output = self.id, "INFO :: Fahrenheit temperature", 9.0/5.0 * temp + 32.0
        return output

    def fahrenheit_celcius(self, temp):
        output = self.id, "INFO :: Celsius temperature", (temp - 32.0) * 5.0/9.0
        return output


ConverterSimple.deploy()
# list current deployment
print(serve.list_deployments()) 


handleSimple = serve.get_deployment('ConverterSimple').get_handle()

print(ray.get(handleSimple.celcius_fahrenheit.remote(333.0)))
print(ray.get(handleSimple.fahrenheit_celcius.remote(333.0)))
print(ray.get(handleSimple.celcius_fahrenheit.remote(222.0)))
print(ray.get(handleSimple.fahrenheit_celcius.remote(222.0)))