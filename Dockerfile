FROM python:3.9.2

# Working directiory
WORKDIR /terminal-chat-server

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY /chat .

# Run the server
CMD ["python", "app.py"]