FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn openai requests pydantic

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
