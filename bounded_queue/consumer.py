import hazelcast
import time


def main():
    client = hazelcast.HazelcastClient()

    # Get a Queue called 'my-distributed-queue'
    queue = client.get_queue("my-distributed-queue").blocking()

    while True:
        result = queue.poll(timeout=10) # wait for 10 seconds.
        # if no values are read in 10 seconds, break
        if result is None:
            break
        print(result)
        time.sleep(2)

if __name__ == "__main__":
    main()
