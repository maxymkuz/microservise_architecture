#!/bin/bash

consul kv put hazelcast_nodes "localhost:5701 localhost:5702 localhost:5703"
consul kv put hazelcast_queue "my-queue"
consul kv put hazelcast_map "distributed-map"