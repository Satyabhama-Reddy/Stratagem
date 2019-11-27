"""
Create  basic flask API that has
	- CPU intensive task
	- Time consuming task
	- Ordinary task
"""
import time
from multiprocessing import Pool
from multiprocessing import cpu_count

from flask import Flask
def f(x):
	for i in range(1000):
		x*x

app = Flask(__name__)



@app.route("/ordinary")
def ordinary():
	return "Hello World!"

@app.route("/cpuIntensive")
def cpuIntensive():
	processes = cpu_count()	
	print(processes)
	pool = Pool(processes*100)
	pool.map(f, range(processes))
	pool.close()
	pool.join()
	return "Hello World!"

@app.route("/timeConsuming/<t>")
def timeConsuming(t):
	time.sleep(int(t))
	return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)