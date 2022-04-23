.PHONY: clean-venv
clean-venv:
	rm -rf __pycache__/
	rm -rf ALERTS/
	rm -rf venv/
	rm -f location.json

.PHONY: build
build: 
	docker build -t weather_monitor .

.PHONY: local-venv
local-venv: clean
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

.PHONY: run-venv-forecast
run-venv:
	./venv/bin/python3 main.py --forecast

.PHONY: run-venv-alerts
run-venv:
	./venv/bin/python3 main.py --alerts

.PHONY: run-docker-forecast
run-docker-forecast:
	docker run -it --rm --user python-user -v $(shell pwd):/home/python-user:rw weather_monitor --forecast 

.PHONY: run-docker-alerts
run-docker-alerts:
	docker run -it --rm --user python-user -v $(shell pwd):/home/python-user/:rw weather_monitor --alerts