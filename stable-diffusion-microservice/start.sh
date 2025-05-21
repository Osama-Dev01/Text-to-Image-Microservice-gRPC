#!/bin/bash
# Start the gRPC server in the background
python server.py &
SERVER_PID=$!

# Wait for the gRPC server to start
sleep 5

# Start the REST gateway (using the local gRPC server)
export GRPC_SERVER=localhost:50051
python rest_gateway.py

# If the REST gateway exits, kill the server
kill $SERVER_PID
