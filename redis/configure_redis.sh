#!/bin/bash

configure_redis() {
  sudo sh -c "echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf"
  sudo sysctl vm.overcommit_memory=1

  sudo sh -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled"
  sudo sh -c "echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' >> /etc/rc.local"
}
