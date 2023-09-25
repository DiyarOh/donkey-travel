PROJECT_NAME=donkeytravel

.PHONY:	start
start:
	docker	compose	up db

.PHONY:	down
down:
	docker	compose	down

