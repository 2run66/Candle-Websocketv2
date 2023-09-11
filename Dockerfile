# Use a base Python image
FROM python:3.8

WORKDIR /app

# Install any system dependencies your application might need (if any)
# For example, if you need to install some system-level packages, do it here

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files into the container
COPY . .

# Expose the ports that your WebSocket servers will use (adjust as needed)
EXPOSE 8080
EXPOSE 8081  # Example, you may have a different port for the other server

# Start your WebSocket servers
CMD ["python", "live_candle_websocket/live_candle_websocket_api.py"]
