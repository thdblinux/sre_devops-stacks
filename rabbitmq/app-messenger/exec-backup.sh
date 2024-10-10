#!/bin/bash

SOLUTION_HOME=${HOME}/app/rabbit-mq
DUMP_DIR=${HOME}/app/rabbit-mq/backup
BACKUP_PREFIX=rabbitmq-bkp
DUMP_FILE=${DUMP_DIR}/${BACKUP_PREFIX}-$(date +%d%m%yT%H%M%S.tar.gz)

mkdir -p "$DUMP_DIR"

docker compose -f docker-compose.yaml down

tar cf "$DUMP_FILE" "$SOLUTION_HOME/docker/data/mnesia"

docker compose -f docker-compose.yaml up -d