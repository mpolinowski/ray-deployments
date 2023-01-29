import ray
from ray import serve
from fastapi import FastAPI
import requests

# start FastAPI
app = FastAPI()
# start Ray
ray.init()
# start Serve
serve.start()

#define deployment
@serve.deployment(route_prefix="/converter")
@serve.ingress(app)
class FastConverter:
    @app.get("/to_fahrenheit")
    def celcius_fahrenheit(self, temp):
        return {"INFO :: Fahrenheit temperature": 9.0/5.0 * float(temp) + 32.0}

    @app.get("/to_celsius")
    def fahrenheit_celcius(self, temp):
        return {"INFO :: Celsius temperature": (float(temp) - 32.0) * 5.0/9.0}

FastConverter.deploy()
# list current deployment
print(serve.list_deployments()) 

# Query our endpoint over HTTP.
print(requests.get("http://127.0.0.1:8000/converter/to_fahrenheit?temp=1111.0&").text)
print(requests.get("http://127.0.0.1:8000/converter/to_celsius?temp=1111.0").text)

#direct invoke
handle = serve.get_deployment('FastConverter').get_handle()

print(ray.get(handle.celcius_fahrenheit.remote(555.0)))
print(ray.get(handle.fahrenheit_celcius.remote(555.0))) 
