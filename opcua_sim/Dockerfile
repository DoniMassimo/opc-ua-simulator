FROM python:3.12
ADD server.py .
ADD opcua_constant.py .
COPY requirements.txt requirements.txt
COPY server_struct.json server_struct.json 
COPY config.json config.json
RUN pip install -r requirements.txt
CMD ["python", "./server.py"] 

