#!/bin/bash
# Ultra-minimalist statusline
# Just the essentials, nothing more

input=$(cat)
M=$(echo "$input" | jq -r '.model.display_name' | head -c 1)
D=$(basename "$(echo "$input" | jq -r '.workspace.current_dir')")
echo "$M:$D"