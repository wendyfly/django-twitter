# need followings in the key, because there are multiple keys for one user id
# the reason that we don't cache the followers key is because you might have millions followers and the followers
# list will refresh more frequently
FOLLOWINGS_PATTERN = 'followings:{user_id}'
