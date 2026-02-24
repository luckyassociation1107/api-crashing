FROM python:3.11-slim

WORKDIR /app

# Requirements install cheyyadam
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Motham code copy cheyyadam
COPY . .

# Bot ni start cheyyadam
CMD ["python", "bot.py"]
