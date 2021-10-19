from redis import Redis
from rq import Queue, SimpleWorker
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

class TSPProblem(object):

    def __init__(self):
       self.locations = []

    def addlocation(self,
                    lat:float,
                    lon:float) -> None:
        self.locations.append((lat,lon))

    def distancematrix(self) -> []:
        ## return here the distance matrix
        matrix = []
        for location in self.locations:
            distances = []
            for olocation in self.locations:
                #Euclidean distance for now
                d = math.sqrt((location[0]-olocation[0])**2 + (location[1]-olocation[1])**2)
                distances.append(d)
            matrix.append(distances)
        return matrix


## specific function implementation of solver for or-tools
def orsolver(distancematrix: []) -> tuple:
    manager = pywrapcp.RoutingIndexManager(len(distancematrix),
                                           1, 0)
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(lambda from_index, to_index:
                                                             distancematrix[manager.IndexToNode(from_index)] \
                                                                 [manager.IndexToNode(to_index)])
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    locorder = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        locorder.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))

    return (locorder, solution.ObjectiveValue())


class TSPSolver(object):

    def __init__(self, redis_host ='localhost', redis_port=6475):
        self._queue = Queue(connection=Redis(host=redis_host, port=redis_port))

    ## solves with a single worker
    def solve(self, problem: TSPProblem, maxseconds = 3) -> tuple:
        job = self._queue.enqueue(orsolver, problem.distancematrix(), result_ttl=maxseconds)
        ## for simplicity use a Simpleworker here
        ## in real scnarios several workers running elsewhere
        worker = SimpleWorker([self._queue], connection=self._queue.connection)
        worker.work(burst=True)  # Runs the job at queue
        return job.result
