curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"strategy":"request load","numberOfRequests":2,"perDuration":10}' \
  http://127.0.0.1:5000/stratagem/scaling