def add_arguments(parser):
    parser.add_argument('--name', type=str, help='Your name')

def execute(args):
    print(f"Hello, {args.name}")
