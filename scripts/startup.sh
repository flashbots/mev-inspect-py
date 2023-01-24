#!/bin/sh
# bash script to launch the
# usage: bash scripts/startup.sh
# this assumes you already ran: kind create cluster
# Do not forget to add your RPC URL below
export RPC_URL=""
tilt down &&
tilt up &&
./mev exec alembic upgrade head &&
./mev prices fetch-all
