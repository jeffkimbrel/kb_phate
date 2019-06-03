#!/bin/bash
/Users/kimbrel1/Science/repos/kb_phate/test_local/run_docker.sh run --rm -v /Users/kimbrel1/Science/repos/kb_phate/test_local/subjobs/$1/workdir:/kb/module/work -v /Users/kimbrel1/Science/repos/kb_phate/test_local/workdir/tmp:/kb/module/work/tmp $4 -e "SDK_CALLBACK_URL=$3" $2 async
