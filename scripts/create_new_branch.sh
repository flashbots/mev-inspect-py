#!/bin/sh
# bash script to create a new branch that respects the library standard
#### ./scripts/create_new_branch.sh "[FEAT] - Implement instrument types #14"
#### ./scripts/create_new_branch.sh "[FEAT] Implement instrument types #14"
#### ./scripts/create_new_branch.sh "[FEAT] - Implement instrument types#14"
base_issue=$1
issue_number=${base_issue##*#}
issue="${base_issue%%#*}"
issue="${issue//\[FEAT\] \- /}"
issue="${issue/\[FEAT\] /}"
issue="${issue/\[FEAT\]/}"
issue="${issue// /\_}"
branch_name="feat/issue-$issue_number ${issue,,}"
branch_name="${branch_name// /\_}"
last_char="${branch_name: -1}"
if [ "$last_char" = "_" ]
then
  branch_name=${branch_name::-1}
fi
git checkout -b $branch_name


