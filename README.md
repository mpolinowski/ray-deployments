## Deployments with Ray

Use Ray to deploy your remote services.


> Source: [Scaling Python with Ray](https://github.com/scalingpythonml/scaling-python-with-ray)


Use __Ray Serve__ for implementing a general-purpose microservice framework and how to use this framework for model serving. __Ray Serve__ is implemented on top of Ray with Ray actors. Three kinds of actors are created to make up a Serve instance:


| Ray Actor | Description |
| -- | -- |
| __Controller__ | The controller is responsible for creating, updating, and destroying other actors. All of the __Serve API__ calls (e.g., creating or getting a deployment) use the controller for their execution. |
| __Router__ | There is one router per node. Each router is a HTTP server that accepts incoming requests, forwards them to replicas, and responds after they are completed. |
| __Worker Replica__ | Worker replicas execute the user-defined code in response to a request. |