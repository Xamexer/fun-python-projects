export NUM_BANKS=3
export NUM_BOURSES=1
python generate_docker_compose.py
docker-compose up --build --remove-orphans
