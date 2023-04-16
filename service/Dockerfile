FROM alpine:3.17.3
RUN apk update && \
        apk add --no-cache python3=3.10.11-r0 py3-pip=22.3.1-r1 && \
        pip install --no-cache-dir bottle==0.12.25
COPY app.py /root/api.py
CMD [ "sh", "-c", "python /root/api.py" ]
EXPOSE 8080
