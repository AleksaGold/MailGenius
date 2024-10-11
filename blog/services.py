from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_posts_from_cache():
    """Получает данные по опубликованным постам блога из кэша, если кэш пустой, получает данные из БД"""
    if not CACHE_ENABLED:
        return Blog.objects.filter(is_published=True)
    posts_from_cache = "blogs_list"
    posts = cache.get(posts_from_cache)
    if posts is not None:
        return posts
    posts = Blog.objects.filter(is_published=True)
    cache.set(posts_from_cache, posts)
    return posts
