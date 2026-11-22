#!/bin/sh
# The daily compatibility run on a client host (cron). Needs Docker and ~/.config/lumibox-compat/env with:
#   E2B_DOMAIN, E2B_API_KEY          the production test account
#   TELEGRAM_TOKEN, TELEGRAM_CHAT    where a failure is reported
# Updates the checkout, builds the image, runs it, reports a failure, and removes what it made.
set -u
dir=$(cd "$(dirname "$0")/.." && pwd)
envfile="$HOME/.config/lumibox-compat/env"
log="$HOME/.local/state/lumibox-compat/$(date -u +%F).log"
mkdir -p "$(dirname "$log")"
. "$envfile"

[ -d "$dir/.git" ] && git -C "$dir" pull -q --ff-only
image=lumibox-compat:run
{
  docker build -q -t "$image" -f "$dir/compat/Dockerfile" "$dir" >/dev/null &&
  docker run --rm --env-file "$envfile" "$image"
} >"$log" 2>&1
status=$?
docker image rm -f "$image" >/dev/null 2>&1
docker builder prune -f --filter until=72h >/dev/null 2>&1
find "$(dirname "$log")" -name '*.log' -mtime +30 -delete

if [ $status -ne 0 ]; then
  tail -c 3000 "$log" | sed 's/[<>&]//g' > "$log.tail"
  curl -s -o /dev/null "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
    --data-urlencode "chat_id=$TELEGRAM_CHAT" \
    --data-urlencode "text=LumiBox examples: daily compatibility run failed on $(hostname) ($log)
$(cat "$log.tail")"
  rm -f "$log.tail"
fi
exit $status
