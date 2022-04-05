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

        while True:
            val = distributed_map.get(key)
            # print(val)
            new_val = val
            time.sleep(0.01) # 10 miliseconds
            new_val += 1
            if distributed_map.replace_if_same(key, val, new_val):
                break

    print(f"Finished! Result = {distributed_map.get(key)}")

    # Shutdown the client.
    client.shutdown()

if __name__ == "__main__":
    main()
