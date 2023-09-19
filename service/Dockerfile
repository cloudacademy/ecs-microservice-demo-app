FROM alpine:3.17.3
RUN apk update && \
        apk add --no-cache python3 py3-pip && \
        pip install --no-cache-dir bottle==0.12.25 aws-xray-sdk==2.12.0
COPY api.py /root/api.py
CMD [ "sh", "-c", "python /root/api.py" ]
EXPOSE 8080
