## Problem description:
For this problem we must develop an API that solves the Traveling Salesman Problem using queues and wrap it in a the form of an API. Use *or-tools* as solver.

## Solution Description
- For this purpose and wrap the problem around a REST API in *rest.py* and communicates in *json*. The API is served by *flask*. 
For the purposes of this excercise this directly served by the flask http server.   
- For the simplicity of this exercise, we used a combination of rq/redis for 
the job queue and SimpleWorkers to just consume and solve the immediate job at hand. 
Ideally, of course, these workers are running in another process or in more robust servers to
solve complex problems.
- The solver (or-tools) is wrapped in classes in *solver.py*, which can be extended for other solvers easily
by changing the backend and adding options or subclasses for these other implementations. This gets
called by the Rest API.
- The application is packaged in docker. 
- The test folder contains a script with tests that can be run with *pytest*.

## REST API Request/Response

The communication format is *json*. The endpoint expects the request in the form:

`
{'locations': [
        {'lat': 1.23, 'lon': 76.56},
        {'lat': 25.412, 'lon': 99.485},
        {'lat': 4.333, 'lon': 12.875},
        {'lat': 94.12, 'lon': 2.112}
    ]}
`

Which is just a list of locations. It returns the solution in the form:

`
 {
    'order': [1, 5, 3, 4],
    'total_distance': 70.68
 }
`

Where *order* is the order of the locations in the solution and *total_distance* 
in the total distance traveled.  For simplicity, used the cartesian distances.

## Running
In the top directory run the _example.sh_ script. This will call docker-compose to build/download images and run the test.

To run the tests, you need pytest. Run `pytest tests` in the top directory.

To run the service standalone, you could just run the *run.py* directly. It will accept the following command line 
arguments:

- host
- port
- redis host
- redis port

## Improvements and TODOs
For the sake of time, simplicity and nature of this excercise not everything was done as it would in production. For example:

- Expose this tiny service behind a mature server (apache/nginx) with uwsgi. The uwsgi configuration has been included
in this exercise and can be activated very simply. See the *Dockerfile*
- Have the job workers in other processes or servers
- The solver base class could be generic and make derived implementation for specific solvers
