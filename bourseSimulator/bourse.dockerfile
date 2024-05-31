FROM python:3.10.10
WORKDIR /app
COPY req.txt req.txt
RUN pip3 install -r req.txt
COPY . /app
CMD python3 bourseSimulation.py FB
