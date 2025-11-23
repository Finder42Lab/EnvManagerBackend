include .env
export

build:
	docker compose -f compose.yaml --env-file ./.env build

ud:
	docker compose -f compose.yaml --env-file ./.env up -d

d:
	docker compose -f compose.yaml down

i:
	docker compose -f compose.yaml run app bash

log:
	docker compose -f compose.yaml logs
