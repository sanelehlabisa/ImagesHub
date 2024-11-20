# Makefile (root)

.PHONY: all run clean

all: backend-build frontend-build

run: backend-run frontend-run

backend-build:
	@$(MAKE) -C backend build

backend-run:
	@$(MAKE) -C backend run

frontend-build:
	@$(MAKE) -C frontend build

frontend-run:
	@$(MAKE) -C frontend run

clean:
	@$(MAKE) -C backend clean
	@$(MAKE) -C frontend clean
