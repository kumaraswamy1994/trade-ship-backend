FROM python:3.11-slim
WORKDIR /app
COPY core/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY core /app
COPY shared_utils /app/shared_utils
ENV PYTHONPATH="/app"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
