.PHONY: up down clean rebuild test

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

clean:
	docker compose down --volumes --remove-orphans
	docker system prune --all --force --volumes
	docker volume prune --force
	docker network prune --force


logs:
	docker compose logs -f