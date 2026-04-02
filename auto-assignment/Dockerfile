FROM python:3.11-slim
WORKDIR /app
COPY auto-assignment/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY auto-assignment /app
COPY shared_utils /app/shared_utils
ENV PYTHONPATH="/app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
