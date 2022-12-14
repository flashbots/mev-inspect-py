#!/bin/sh
#  commits and push
branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
./scripts/commit.sh
git push --set-upstream origin $branch