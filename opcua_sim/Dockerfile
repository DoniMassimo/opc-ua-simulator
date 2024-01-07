FROM python:3.12
ADD ./server_init.py ./server_init.py
ADD ./server/opcua_constant.py ./server/opcua_constant.py
ADD ./test_project/ ./test_project/
ADD ./server/server.py ./server/server.py
ADD ./test_project/server/config.json ./test_project/server/config.json
ADD ./utils/utils.py ./utils/utils.py
ADD ./utils/global_const.py ./utils/global_const.py
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "./server_init.py"] 

