ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python deps
RUN apk add --no-cache python3 py3-pip py3-smbus i2c-tools \
    && pip3 install --no-cache-dir RPi.GPIO smbus2

WORKDIR /app
COPY x728_daemon.py .
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
