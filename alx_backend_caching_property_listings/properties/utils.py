from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        logger.info("Cache miss: fetching properties from DB")
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, 3600)  # 1 hour
    else:
        logger.info("Cache hit: properties retrieved from cache")
    return properties

def get_redis_cache_metrics():
    from django_redis import get_redis_connection

    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = hits / total if total > 0 else None

    logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio}")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }
