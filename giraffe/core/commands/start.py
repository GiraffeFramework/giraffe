import argparse


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("--host", default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")


def execute(args):
    print(f"Starting server on {args.host}:{args.port}")
    # Your logic to start the server
    # from giraffe.core.app import start_server
    # start_server(args.host, args.port)
