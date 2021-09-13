#!/bin/bash

cd "$(dirname "$0")"

export SOME_TOKEN=abc123

set -ex
tilt ci
tilt down --delete-namespaces
