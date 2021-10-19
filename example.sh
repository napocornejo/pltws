#/bin/bash
set -e

docker-compose up -d
pip install pytest
pytest tests