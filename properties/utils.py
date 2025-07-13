from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        logger.info("Cache miss: fetching properties from DB")
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    else:
        logger.info("Cache hit: properties retrieved from cache")
    return properties


def get_redis_cache_metrics():
    from django_redis import get_redis_connection

    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = hits / total_requests if total_requests > 0 else 0


        logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

    except Exception as e:

        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0
        }
