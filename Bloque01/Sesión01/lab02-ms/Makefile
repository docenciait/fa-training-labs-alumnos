.PHONY: up down rebuild logs

up:
	docker-compose up --build -d

down:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

clean:
	docker compose down --volumes --remove-orphans
	docker system prune --all --force --volumes
	docker volume prune --force
	docker network prune --force

logs:
	docker-compose logs -f --tail=100
