from random import random
import requests
import ray
from ray import serve

ray.init()
serve.start()

@serve.deployment
def version_one(data):
    return {"version": "I am the old version..."}

version_one.deploy()

@serve.deployment
def version_two(data):
    return {"version": "I am the new version!"}

version_two.deploy()

@serve.deployment(route_prefix="/get_version")
class Canary:
    def __init__(self, canary_percent):
        from random import random
        self.version_one = version_one.get_handle()
        self.version_two = version_two.get_handle()
        self.canary_percent = canary_percent

    # This method can be called concurrently!
    async def __call__(self, request):
        data = await request.body()
        if(random() > self.canary_percent):
            return await self.version_one.remote(data=data)
        else:
            return await self.version_two.remote(data=data)

# invocation with canary_percent of 30%
Canary.deploy(.3)

# call api 10 times
for _ in range(10):
    resp = requests.get("http://127.0.0.1:8000/get_version", data="some string, doesn't matter")
    print(resp.json())