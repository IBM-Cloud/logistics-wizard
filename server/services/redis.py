from __future__ import absolute_import

from redis import Redis
from urlparse import urlparse

from server.config import Config

redis_url = urlparse(Config.REDIS_URL)

# setup the redis connection
redis = Redis(
    host=redis_url.hostname,
    port=redis_url.port,
    password=redis_url.password,
    socket_timeout=5,
    socket_connect_timeout=5
)