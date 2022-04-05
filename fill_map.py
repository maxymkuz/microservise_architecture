import random
import hazelcast

# Connect to Hazelcast cluster.
client = hazelcast.HazelcastClient()

# Get or create the "distributed-map" on the cluster.
distributed_map = client.get_map("distributed-map")

# Put "key", "value" pair into the "distributed-map" and wait for
# the request to complete.
for i in range(1000):
    distributed_map.set(i, str(random.randint(0, 1000000))).result()


print("Map size:", distributed_map.size().result())

# Shutdown the client.
client.shutdown()