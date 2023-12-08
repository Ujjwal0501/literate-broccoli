import os


MAX_REQUEST_SIZE = 1000
PORT = int(os.environ['PORT']) if 'PORT' in os.environ else 5000
CACHE_DURATION = int(os.environ['CACHE_DURATION']) if 'CACHE_DURATION' in os.environ else 20
DB_POLL = int(os.environ['DB_POLL']) if 'DB_POLL' in os.environ else 1

