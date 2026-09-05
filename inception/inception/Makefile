NAME        = inception
COMPOSE_FILE = ./srcs/docker-compose.yml

all: build up

build:
	@mkdir -p /home/mewaysi/data/wordpress
	@mkdir -p /home/mewaysi/data/mariadb
	docker compose -f $(COMPOSE_FILE) build

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

stop:
	docker compose -f $(COMPOSE_FILE) stop

clean: down
	docker system prune -a --force

fclean: clean
	docker volume rm $$(docker volume ls -q) 2>/dev/null || true
	sudo rm -rf /home/mewaysi/data

re: fclean all

.PHONY: all build up down stop clean fclean re
