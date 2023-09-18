FROM debian:10-slim

# Set working dir to /app
WORKDIR /app

# Copy the xmr-code into container and install required packages
RUN apt-get update && apt-get install -y git build-essential cmake libuv1-dev libssl-dev libhwloc-dev && git clone https://github.com/xmrig/xmrig.git && mkdir xmrig/build && cd xmrig/build && cmake .. && make -j$(nproc)



