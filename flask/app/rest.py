from app import app
from app.solver import TSPProblem, TSPSolver
from flask import request, abort,jsonify

@app.route("/api/v0.1/solver/tsp", methods=['GET','POST'])
def solvetsp():
    data = request.get_json()
    ## expect a list o lat/lon coordinates
    if 'locations' not in data:
        abort(400, 'No locations field')

    tprob = TSPProblem()
    for location in data['locations']:
        if ('lat' not in location) or ('lon' not in location):
            abort(400, 'No proper lat/lon')

        tprob.addlocation(location['lat'], location['lon'])

    try:
        psolv = TSPSolver(redis_host=app.config['REDIS_HOST'],
                          redis_port=app.config['REDIS_PORT'])
        result = psolv.solve(tprob)

        if result is None:
            abort(500, 'No solution in time.')

        solution = {
            'order': result[0],
            'total_distance': result[1]
        }
        print(solution)
        return jsonify(solution)

    except Exception as e:
        abort(500, str(e))


