all:
	@echo "Need default python3 to run this program."
	@echo "make setup: generate file data for peers"
	@echo "make test: runts test.sh scrip with given peers"
	@echo "make clean: remove all files for peers, log data and config files"

setup:
	python3 filegenerator.py
	echo p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 p17 | xargs -n 1 cp -r p1

test:
	@echo "Run tests:"
	@echo "Running download from 2 clients"
	@bash test.sh 2
	@echo "Running download from 4 clients"
	@bash test.sh 4
	@echo "Running download from 8 clients"
	@bash test.sh 8
	@echo "Running download from 16 clients"
	@bash test.sh 16

clean:
	@rm -rf p1 p2 p3 p4 p5 p6 p7 p8 p9 p1*
	@rm -f logs/*
	@rm -f configs/*
