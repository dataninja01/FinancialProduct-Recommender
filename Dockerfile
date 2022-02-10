FROM python:3.8
RUN apt-get update
RUN cd $HOME
RUN git clone -b deploy_branch_4 https://github.com/dataninja01/Capstone-Project
RUN cd Capstone-Project
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN python3 server.py
EXPOSE 8080
CMD ["python3", "server.py", "serve"]
