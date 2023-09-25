# base image
FROM openjdk:11

# define spark and hadoop versions
ENV SPARK_VERSION=3.3.3
ENV HADOOP_VERSION=3.3.1

# download and install hadoop
ENV HADOOP_HOME /opt/hadoop-${HADOOP_VERSION}
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
ENV LD_LIBRARY_PATH /opt/hadoop/lib/native/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH ${HADOOP_HOME}/lib/native/:$LD_LIBRARY_PATH

RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz -O && \
    tar -xvzf ./hadoop-${HADOOP_VERSION}.tar.gz && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native


# download and install spark
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -O && \
        tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop3 spark && \
    echo Spark ${SPARK_VERSION} installed in /opt

# Setting Env Variables for Hadoop and Spark
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo "export HDFS_NAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo "export HDFS_DATANODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo "export HDFS_SECONDARYNAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo "export YARN_RESOURCEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo "export YARN_NODEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
# Env Variables for Spark
ENV SPARK_HOME /opt/spark-${SPARK_VERSION}-bin-hadoop3
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV PATH $PATH:${SPARK_HOME}/bin:${SPARK_HOME}/sbin

# SSH Install
RUN apt-get update && \ 
    apt-get install -y less
RUN apt-get -y install vim
RUN apt-get -y install ssh
RUN apt-get -y install openssh-server
RUN apt-get -y install openssh-client
RUN apt-get -y install rsync
RUN apt-get -y install net-tools
RUN apt-get update && \
    apt-get -y install sudo

# add scripts and update spark default config
COPY /tests/test.py /home/
COPY /tests/TGN_Entrega_GBA_Agosto.csv /home/
ADD common.sh spark-master spark-worker /
ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin
ENV PATH $PATH:$HADOOP_HOME/sbin

# Create HDFS directories
RUN mkdir -p /data/hadoop-master
RUN mkdir -p /data/hadoop-slave

COPY /hadoop-conf/core-site.xml ${HADOOP_CONF_DIR}
COPY /hadoop-conf/hdfs-site.xml ${HADOOP_CONF_DIR}
COPY /hadoop-conf/mapred-site.xml ${HADOOP_CONF_DIR}
COPY /hadoop-conf/yarn-site.xml ${HADOOP_CONF_DIR}

# node manager ports
EXPOSE 9000
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