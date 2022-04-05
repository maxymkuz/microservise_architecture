import random
import hazelcast

client = hazelcast.HazelcastClient()

# Get or create the "distributed-map" on the cluster.
distributed_map = client.get_map("distributed-map").blocking()

key = "1"

distributed_map.put(key, 0)



# Shutdown the client.
client.shutdown()