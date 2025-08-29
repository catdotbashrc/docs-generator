#!/bin/bash
# DDD Command Wrapper - Enables automatic memory updates

DDD_COMMAND="$1"
shift

case "$DDD_COMMAND" in
    "measure")
        # Run measure and trigger hook
        ddd measure "$@"
        RESULT=$?
        python .serena/hooks/trigger_hook.py "post_measure" "$@"
        exit $RESULT
        ;;
    "assert-coverage")
        # Run assert and trigger hook
        ddd assert-coverage "$@"
        RESULT=$?
        if [ $RESULT -ne 0 ]; then
            python .serena/hooks/trigger_hook.py "post_assert_failure" "$@"
        fi
        exit $RESULT
        ;;
    "demo")
        # Run demo and trigger hook
        ddd demo "$@"
        RESULT=$?
        python .serena/hooks/trigger_hook.py "post_demo" "$@"
        exit $RESULT
        ;;
    *)
        # Pass through other commands
        ddd "$DDD_COMMAND" "$@"
        ;;
esac
