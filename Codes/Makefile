setup:
	python3 filegenerator.py
	echo p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 p17 | xargs -n 1 cp -r p1

test:
	@echo "Run tests:"
	@echo "Running download from 2 clients"
	bash test.sh 2
	@echo "Running download from 4 clients"
	bash test.sh 4
	@echo "Running download from 8 clients"
	bash test.sh 8
	@echo "Running download from 16 clients"
	bash test.sh 16
	mv -rf 2test* 4test* 8test* 16test* test-logs

clean:
	rm -rf p1 p2 p3 p4 p5 p6 p7 p8 p9 p1*
	rm logs/*
	rm configs/*
