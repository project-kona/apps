#!/bin/bash

# install deps
###########################
install_deps() {
  sudo apt-get install -y build-essential autoconf automake \
        libpcre3-dev libevent-dev pkg-config \
        zlib1g-dev tcl8.6 libssl-dev
}

# Redis
##########################
install_redis() {
  git clone https://github.com/antirez/redis
  pushd redis 
    make distclean # important! 
    make -j$(nproc)

    # Use already-provided Redis file
    cp ../redis-memory.conf ./redis.conf
  popd
}

configure_redis() {
  sudo sh -c "echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf"
  sudo sysctl vm.overcommit_memory=1

  sudo sh -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled"
  sudo sh -c "echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' >> /etc/rc.local"
  sudo sh -c "echo 1024 > /proc/sys/net/core/somaxcon"
}


# Memtier
##########################
install_memtier() {
  git clone https://github.com/RedisLabs/memtier_benchmark
  pushd memtier_benchmark
    autoreconf -ivf
    ./configure
    make $(nproc)
    sudo make install
  popd
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd ${SCRIPT_DIR}
install_redis
configure_redis
install_memtier