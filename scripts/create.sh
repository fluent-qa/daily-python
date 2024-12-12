#!/bin/sh
PROJECT_NAME=$1

mkdir ${PROJECT_NAME} && cd ${PROJECT_NAME}
pdm init https://github.com/fluent-qa/fluentqa-pytpl.git
