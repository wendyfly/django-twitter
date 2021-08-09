# need followings in the key, because there are multiple keys for one user id
# the reason that we don't cache the followers key is because you might have millions followers and the followers
# list will refresh more frequently
# memcached
FOLLOWINGS_PATTERN = 'followings:{user_id}'
USER_PATTERN = 'user:{user_id}'
# we don't user profile id, we use user id because we usually use user id to look for a profile as foreign key
USER_PROFILE_PATTERN = 'userprofile:{user_id}'

# redis
USER_TWEETS_PATTERN = 'user_tweets:{user_id}'
USER_NEWSFEEDS_PATTERN = 'user_newsfeeds:{user_id}'