#!/usr/bin/env bash
# wait-for-it.sh

# Usage: ./wait-for-it.sh host:port [-- command args]
#   -h HOST | --host=HOST       Host or IP under test
#   -p PORT | --port=PORT       TCP port under test
#   Alternatively, you can use the first positional argument as host:port
#   -q | --quiet                Don't output any status messages
#   -t TIMEOUT | --timeout=TIMEOUT
#                               Timeout in seconds, zero for no timeout
#   -- COMMAND ARGS             Execute command with args after the test finishes

TIMEOUT=25
QUIET=0
HOST=
PORT=
echoerr() { if [[ $QUIET -eq 0 ]]; then echo "$@" 1>&2; fi }

usage() {
  exitcode="$1"
  cat << USAGE >&2
Usage:
$0 host:port [-q] [-t timeout] [-- command args]
  -q | --quiet                        Do not output any status messages
  -t TIMEOUT | --timeout=TIMEOUT      Timeout in seconds, zero for no timeout
  -h HOST | --host=HOST               Host or IP under test
  -p PORT | --port=PORT               TCP port under test
  -- COMMAND ARGS                     Execute command with args after the test finishes
USAGE
  exit "$exitcode"
}

wait_for() {
  if [[ $TIMEOUT -gt 0 ]]; then
    echoerr "$0: waiting $TIMEOUT seconds for $HOST:$PORT"
  else
    echoerr "$0: waiting for $HOST:$PORT without a timeout"
  fi
  start_ts=$(date +%s)
  while :
  do
    if [[ $TIMEOUT -gt 0 ]]; then
      current_ts=$(date +%s)
      elapsed=$(( current_ts - start_ts ))
      if [[ $elapsed -ge $TIMEOUT ]]; then
        echoerr "$0: timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT"
        return 1
      fi
    fi
    nc -z "$HOST" "$PORT" >/dev/null 2>&1 && break
    sleep 1
  done
  return 0
}

parse_arguments() {
  while [[ $# -gt 0 ]]
  do
    case "$1" in
      -q | --quiet)
      QUIET=1
      shift 1
      ;;
      -t)
      TIMEOUT="$2"
      if [[ $TIMEOUT == "" ]]; then break; fi
      shift 2
      ;;
      --timeout=*)
      TIMEOUT="${1#*=}"
      shift 1
      ;;
      -h)
      HOST="$2"
      if [[ $HOST == "" ]]; then break; fi
      shift 2
      ;;
      --host=*)
      HOST="${1#*=}"
      shift 1
      ;;
      -p)
      PORT="$2"
      if [[ $PORT == "" ]]; then break; fi
      shift 2
      ;;
      --port=*)
      PORT="${1#*=}"
      shift 1
      ;;
      --)
      shift
      COMMAND="$@"
      break
      ;;
      -*)
      echoerr "Unknown argument: $1"
      usage 1
      ;;
      *)
      if [[ "$HOST" == "" && "$PORT" == "" ]]; then
        HOSTPORT=(${1//:/ })
        HOST=${HOSTPORT[0]}
        PORT=${HOSTPORT[1]}
      else
        COMMAND="$@"
      fi
      shift
      ;;
    esac
  done
}

parse_arguments "$@"

if [[ "$HOST" == "" || "$PORT" == "" ]]; then
  echoerr "Error: you need to provide a host and port to test."
  usage 2
fi

wait_for

if [[ $? -eq 0 ]]; then
  echoerr "$0: $HOST:$PORT is available after $(( elapsed )) seconds"
  exec $COMMAND
else
  echoerr "$0: $HOST:$PORT is not available"
  exit 1
fi