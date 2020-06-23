FROM centos:7

ARG ROOT_PASS=luan123

RUN yum -y install openssh-server

# 空パスワードの場合は以下をコメントアウト
RUN sed -ri 's/^#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

# 任意のパスワードの場合は以下をコメントアウト & パスワードを書き換える
RUN echo 'root:'$ROOT_PASS | chpasswd

RUN yum groupinstall -y "Development Tools"
RUN yum install -y \
  libffi-devel \
  zlib-devel \
  bzip2-devel \
  openssl-devel \
  ncurses-devel \
  sqlite-devel \
  readline-devel \
  tk-devel \
  gdbm-devel \
  db4-devel \
  libpcap-devel \
  xz-devel \
  expat-devel \
  postgresql-devel \
  wget \
  nano
  
RUN yum -y install httpd

RUN yum -y install git

RUN yum -y install python-devel httpd-devel rsyslog

RUN systemctl enable httpd.service

WORKDIR /opt
RUN wget http://python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
RUN tar xf Python-3.7.2.tar.xz
WORKDIR /opt/Python-3.7.2
RUN ./configure --enable-shared --prefix=/opt/python3.7 LDFLAGS=-Wl,-rpath=/opt/python3.7/lib --enable-optimizations
RUN make altinstall

WORKDIR /opt

RUN mv /etc/localtime /etc/localtime.pk

RUN ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

EXPOSE 80 22

CMD /usr/sbin/init