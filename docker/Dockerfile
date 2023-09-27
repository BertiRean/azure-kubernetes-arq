# Get base image
FROM ubuntu:20.04

# Install Java
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    add-apt-repository ppa:openjdk-r/ppa -y && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get clean

# Install needed packages
RUN apt-get install less -y
RUN apt-get -y install nano
RUN apt-get -y install vim
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install openssh-client
RUN apt-get -y install rsync
RUN apt-get update && \
      apt-get -y install sudo
RUN apt install -y python3-venv python3-pip
RUN useradd -ms /bin/bash sparker
RUN usermod -aG sudo sparker
RUN passwd -d sparker

# Python Link
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install pyspark

USER sparker
WORKDIR /home/sparker

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre/

# Download Spark binary distribution with Hadoop
ENV HADOOP_VERSION 3.3.2
ENV HADOOP_HOME /home/sparker/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz  -q -O ./hadoop-$HADOOP_VERSION.tar.gz
RUN tar -xvzf ./hadoop-$HADOOP_VERSION.tar.gz
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
ENV LD_LIBRARY_PATH ${HADOOP_HOME}/lib/native/:$LD_LIBRARY_PATH

# SPARK
ENV SPARK_VERSION 3.3.2
ENV SPARK_HOME /home/sparker/spark-$SPARK_VERSION-bin-hadoop3
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV PATH $PATH:${SPARK_HOME}/bin:${SPARK_HOME}/sbin
RUN wget https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz -q -O ./spark-$SPARK_VERSION-bin-hadoop3.tgz
RUN tar -xvzf ./spark-$SPARK_VERSION-bin-hadoop3.tgz

# node manager ports
EXPOSE 8040
EXPOSE 8042
EXPOSE 22
EXPOSE 8030
EXPOSE 8031
EXPOSE 8032
EXPOSE 8033
EXPOSE 8088
EXPOSE 10020
EXPOSE 19888

# add scripts and update spark default config
COPY /tests/test.py /home/sparker/
COPY /tests/TGN_Entrega_GBA_Agosto.csv /home/sparker/
COPY /tests/test.xlsx /home/sparker/
ADD common.sh spark-master spark-worker /home/sparker/
ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin
ENV PATH $PATH:$HADOOP_HOME/sbin

USER root 
RUN chmod +x /home/sparker/common.sh
RUN chmod +x /home/sparker/spark-master
RUN chmod +x /home/sparker/spark-worker

USER sparker

# Create HDFS directories
RUN mkdir -p /home/sparker/hdfs-hadoop/namenode
RUN mkdir -p /home/sparker/hdfs-hadoop/datanode

# Copy Hadoop Conf Files
COPY ./hadoop-conf/core-site.xml ./hadoop-$HADOOP_VERSION/etc/hadoop
COPY ./hadoop-conf/yarn-site.xml ./hadoop-$HADOOP_VERSION/etc/hadoop
COPY ./hadoop-conf/hdfs-site.xml ./hadoop-$HADOOP_VERSION/etc/hadoop
COPY spark-defaults.conf ./spark-$SPARK_VERSION-bin-hadoop3/conf
RUN $HADOOP_HOME/bin/hdfs namenode -format

# node manager ports
EXPOSE 8040
EXPOSE 8042
EXPOSE 22
EXPOSE 8030
EXPOSE 8031
EXPOSE 8032
EXPOSE 8033
EXPOSE 8088
EXPOSE 10020
EXPOSE 19888
EXPOSE 7077
EXPOSE 8080

