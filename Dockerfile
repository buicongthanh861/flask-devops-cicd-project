FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=install -r requirements.txt

#run statement
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app/install /usr/local
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]



