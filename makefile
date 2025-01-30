PYTHON := python3

all: run

run:
	$(PYTHON) ImageDownloader.py
	$(PYTHON) ImageLabel.py
	$(PYTHON) Tertile.py
	$(PYTHON) datacleaning.py
	$(PYTHON) rate.py
	$(PYTHON) main.py > output.txt

clean:
	rm -f output.txt
