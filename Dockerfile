FROM python:3.12.1-slim

# Set workdir
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Install system dependencies (including unzip)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    aria2 \
    wget \
    unzip \
    build-essential \
    cmake \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Build and install Bento4 mp4decrypt
RUN wget -O Bento4-SDK.zip https://github.com/axiomatic-systems/Bento4/archive/refs/heads/master.zip && \
    unzip Bento4-SDK.zip && \
    cd Bento4-master && \
    mkdir build && cd build && \
    cmake .. && \
    make mp4decrypt && \
    cp mp4decrypt /usr/local/bin/ && \
    cd ../.. && \
    rm -rf Bento4-SDK.zip Bento4-master

# 3. Leverage Docker caching for Python dependencies
COPY master.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r master.txt

# 4. Copy application source code
COPY . .

CMD ["python", "main.py"]
