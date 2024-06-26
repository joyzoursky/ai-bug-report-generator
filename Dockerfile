FROM python:3.9-slim

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

COPY index.html /usr/local/lib/python3.9/site-packages/streamlit/static/index.html

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/chatbot.py", "--server.port=8501", "--server.address=0.0.0.0", "--client.toolbarMode=minimal"]