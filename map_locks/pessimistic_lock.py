import hazelcast
import time

def main():
    # Connect to Hazelcast cluster.
    client = hazelcast.HazelcastClient()

    # Get or create the "distributed-map" on the cluster.
    distributed_map = client.get_map("distributed-map").blocking()

    key = "1"

    for k in range(1000):
        if k % 100 == 0:
            print(f"at: {k}")

        distributed_map.lock(key)
        val = distributed_map.get(key)
        time.sleep(0.01) # 10 miliseconds
        # print(val)
        val += 1
        distributed_map.put(key, val)
        distributed_map.unlock(key)

    print(f"Finished! Result = {distributed_map.get(key)}")

    # Shutdown the client.
    client.shutdown()

if __name__ == "__main__":
    main()
