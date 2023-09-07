FROM python:3.8

WORKDIR /app
# Create a virtual environment named 'venv'
RUN python -m venv venv

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Add your scripts
COPY kline_websocket/candle-websocket-api.py .
COPY commons/commons.py .

CMD ["python", "candle-websocket-api.py"]
