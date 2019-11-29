FROM alpine:3.7
COPY exampleServer.py /exampleServer.py
COPY runner.sh /runner.sh

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip 
RUN pip3 install flask
EXPOSE 5000

CMD ["./runner.sh"]
