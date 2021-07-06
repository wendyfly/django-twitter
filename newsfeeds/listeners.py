def push_newsfeed_to_cache(sender, instance, created, **kwargs):
    # in case we save the same feed multiple times
    if not created:
        return
    from newsfeeds.services import  NewsFeedService
    NewsFeedService.push_newsfeed_to_cache(instance)