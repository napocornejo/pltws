from app import app
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help="Host", default="0.0.0.0")
    parser.add_argument('--port', type=int, help="Port Number", default=9999)
    parser.add_argument('--redis_host', type=str, help="Redis Host")
    parser.add_argument('--redis_port', type=int, help="Redis Port")
    args = parser.parse_args()

    app.config['REDIS_HOST'] = args.redis_host
    if args.redis_host is None:
        app.config['REDIS_HOST'] = 'localhost'
        if 'REDIS_HOST' in os.environ:
            app.config['REDIS_HOST'] = os.environ['REDIS_HOST']

    print(f'Redis Host: {app.config["REDIS_HOST"]}')

    app.config['REDIS_PORT'] = args.redis_port
    if args.redis_port is None:
        app.config['REDIS_PORT'] = 6379
        if 'REDIS_PORT' in os.environ:
            app.config['REDIS_PORT'] = int(os.environ['REDIS_PORT'])

    print(f'Redis Port: {app.config["REDIS_PORT"]}')

    app.run(host=args.host, port=args.port, debug=False,
            threaded=False, processes=10)