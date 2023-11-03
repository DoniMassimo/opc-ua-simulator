FROM python:3.12
ADD ./Server/start.py ./Server/start.py
ADD ./Server/opcua_constant.py ./Server/opcua_constant.py
ADD ./server_data/server_struct.json ./server_data/server_struct.json
ADD ./Server/server.py ./Server/server.py
ADD ./Client/config.json ./Client/config.json 
ADD requirements.txt requirements.txt
# COPY ./server_data/server_struct.json ./server_data/server_struct.json
# COPY ./Server/server.py ./Server/server.py
# COPY ./Client/config.json ./Client/config.json 
RUN pip install -r requirements.txt
CMD ["python", "./Server/start.py"] 

