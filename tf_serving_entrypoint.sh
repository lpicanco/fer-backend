#!/bin/bash 
BIND_PORT=${PORT:-8501}
tensorflow_model_server --port=8500 --rest_api_port=${BIND_PORT} --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME} "$@"