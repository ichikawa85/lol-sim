from riotwatcher import RiotWatcher, ApiError

watcher = RiotWatcher('RGAPI-2875d759-03f7-4ea6-a767-c59432dd7df4')

my_region = 'jp1'

me = watcher.summoner.by_name(my_region, 'matarooo')
print(me)

# all objects are returned (by default) as a dict
# lets see if I got diamond yet (I probably didn't)
my_ranked_stats = watcher.league.positions_by_summoner(my_region, me['id'])
print(my_ranked_stats)

# Lets get some champions
static_champ_list = watcher.static_data.champions(my_region)
print(static_champ_list)

# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

try:
    response = watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise
