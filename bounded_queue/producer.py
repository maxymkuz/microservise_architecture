import hazelcast
import time


def main():
    client = hazelcast.HazelcastClient()

    # Get a Queue called 'my-distributed-queue'
    queue = client.get_queue("my-distributed-queue").blocking()
    queue.clear()
    for i in range(101):
        added = False
        while not added:
            added = queue.offer(i)
            if queue.remaining_capacity() > 0:
                print(f"Capacity remaining: {queue.remaining_capacity()}")
            else:
                print("Queue is full, waiting for customers to read")
            time.sleep(1)
            if added:
                print(f"Produced number {i}")
    time.sleep(10)


if __name__ == "__main__":
    main()
