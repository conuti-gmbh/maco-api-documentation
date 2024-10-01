#!/bin/bash

# Set the log file
LOG_FILE="logs/auto-update-schema.log"

rm -rf bo4e-schema/  && \
git clone git@github.com:conuti-gmbh/bo4e-schema.git && \
cp -r bo4e-schema/schemas/v1 bo4e/components/schemas && \
rm -rf bo4e-schema/ && \
python3 scripts/remove_unused_key_in_schemas.py >> $LOG_FILE 2>&1 && \ 
./scripts/build-openapi-json.sh >> $LOG_FILE 2>&1 
git add . && \
git commit -m "update schemas from bo4e-schema" && \
git push