FROM python:3.8.7-buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN apt-get install -y sox
# RUN apt-get install -y gcc-multilib g++-multilib
RUN apt install build-essential -y
RUN apt-get install manpages-dev -y

RUN apt-get install -y libpq-dev
RUN apt-get install -y libsndfile1
RUN apt-get install -y libpcap-dev
RUN apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran
RUN apt-get install -y zip unzip


RUN mkdir /opt/ekstep_data_pipelines/
WORKDIR /opt/ekstep_data_pipelines/


COPY requirements.txt .
COPY lib/wada_snr.tar.gz .
COPY ekstep_data_pipelines /opt/ekstep_data_pipelines/ekstep_data_pipelines
COPY invocation_script.py /opt/ekstep_data_pipelines

RUN tar -xzvf wada_snr.tar.gz

RUN mkdir -p /opt/ekstep_data_pipelines/ekstep_data_pipelines/binaries/
RUN mv WadaSNR /opt/ekstep_data_pipelines/ekstep_data_pipelines/binaries/
RUN ls /opt/ekstep_data_pipelines/ekstep_data_pipelines/binaries/WadaSNR/
RUN rm wada_snr.tar.gz


RUN python -m pip install --upgrade pip

RUN python --version ; pip --version

RUN pip install --upgrade setuptools
RUN pip install -U setuptools
RUN pip install cython

RUN pip install -r requirements.txt

# CMD ["sh", "-c", "tail -f /dev/null"]