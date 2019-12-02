#!/bin/bash

curl http://127.0.0.1:5000/cpuIntensive
sleep 1
curl http://127.0.0.1:5000/cpuIntensive
sleep 1
curl http://127.0.0.1:5000/cpuIntensive
sleep 1

curl http://127.0.0.1:5000/ordinary
