FROM alpine:3.17.3
RUN apk update && \
	apk add --no-cache python3 py3-pip && \
	pip install --no-cache-dir bottle==0.12.25 requests==2.28.2 jinja2==3.1.2 aws-xray-sdk==2.12.0
COPY app.py /root/app.py
COPY index.html /root/index.html
COPY static/pico.css /root/static/pico.css
CMD [ "sh", "-c", "python /root/app.py" ]
EXPOSE 8080
