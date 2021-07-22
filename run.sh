#!/bin/bash

# Ah, ha, ha, ha, stayin' alive...
while :; do :; done & kill -STOP $! && wait $!
