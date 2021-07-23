#!/bin/bash

# Source: https://github.com/docker/compose/issues/1926#issuecomment-505294443

# Ah, ha, ha, ha, stayin' alive...
while :; do :; done & kill -STOP $! && wait $!
