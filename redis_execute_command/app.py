import redis
import os

def lambda_handler(event, context):
    #Check whether we are reading or writing
    commandType = event["query"]
    retVal = []
    #Connect to Redis
    r = get_redis_client()
    if commandType == "RedisSet":
        #If this is a mutation command, we expect an array of arrays, each containing a Redis command and paramters
        pipe = r.pipeline()
        #Create a Redis pipeline 
        for cmd in event["context"]["arguments"]["Command"]:
            #Add commands into the pipeline
            sCMD = makeArgStr(cmd)
            pipe.execute_command(sCMD)
        #Execute the set of commands
        retVal = formatRedisReply(pipe.execute())
    if commandType == "RedisGet":
        #If this is a query, execute the Redis command and return the result(s)
        sCMD = makeArgStr(event["context"]["arguments"]["Command"])
        retVal = formatRedisReply(r.execute_command(sCMD))
    #Close the Redis connection 
    r.close()
    return retVal


def formatRedisReply(redisReply):
    if isinstance(redisReply,list):
        return redisReply
    else:
        retArr=[]
        retArr.append(redisReply)        
        return retArr

def makeArgStr(arr):
    sCMD = ""
    for str in arr:
        sCMD = sCMD + " " + str
    return sCMD

def get_redis_client():
    return redis.Redis(host=os.getenv('REDIS_MASTER_HOST'), port=os.getenv('REDIS_MASTER_PORT'), db=0, decode_responses=True)

    