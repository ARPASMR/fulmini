FROM conda/miniconda2
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install vim
RUN apt-get -y install curl
RUN conda install cartopy
RUN conda install pandas
RUN pip install minio
RUN pip install Pillow
RUN pip install flask
WORKDIR /usr/src/myapp
COPY *.py ./
COPY *.sh ./
COPY province.* ./
COPY Reg_2016_L*.* ./
RUN mkdir templates
RUN touch file_controllo.txt
COPY templates/* templates/
RUN mkdir static
RUN mkdir static/js
COPY static/* static/
COPY static/js/* static/js/
#CMD ["./launch.sh", "600"]
