from rq.cli import worker
from server.data import wire_models

if __name__ == '__main__':
    wire_models()
    worker()