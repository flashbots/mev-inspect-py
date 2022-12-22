#!/bin/sh
# bash script to commit in accordance with the branch name
# usage: ./scripts/commit.sh
branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
branch="${branch##*feat/}"
branch="${branch//\_/ }"
issue_number="${branch//issue\-/}"
title=$( cut -d ' ' -f 2- <<< "$issue_number" )
issue_number=$( cut -d ' ' -f 1 <<< "$issue_number" )
commit_message="feat: $title - closes #$issue_number"
git commit -sam "$commit_message"