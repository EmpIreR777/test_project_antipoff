FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "python migrations.py && uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload"]

# docker build -t goods_sales_analyzes_build .
# docker run -d -p 5000:5000 --name goods_sales_analyzes_container goods_sales_analyzes_build
# docker logs goods_sales_analyzes_container
