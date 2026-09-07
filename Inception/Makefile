NAME         = inception
COMPOSE_FILE = ./srcs/docker-compose.yml
ENV_FILE     = ./srcs/.env
DATA_PATH    = /home/mewaysi/data

all: build up

build:
	@mkdir -p $(DATA_PATH)/wordpress
	@mkdir -p $(DATA_PATH)/mariadb
	docker compose -p $(NAME) -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build

up:
	@mkdir -p $(DATA_PATH)/wordpress
	@mkdir -p $(DATA_PATH)/mariadb
	docker compose -p $(NAME) -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d

down:
	docker compose -p $(NAME) -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down

stop:
	docker compose -p $(NAME) -f $(COMPOSE_FILE) --env-file $(ENV_FILE) stop

clean: down
	docker system prune -f

fclean:
	docker compose -p $(NAME) -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down -v --rmi all 2>/dev/null || true
	docker volume rm mariadb_data wordpress_data 2>/dev/null || true
	docker system prune -a --force
	sudo rm -rf $(DATA_PATH)

re: fclean all

.PHONY: all build up down stop clean fclean re
