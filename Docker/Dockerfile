# Build Ubuntu image with base functionality.
FROM ubuntu:23.04 as builder
MAINTAINER John Zhao

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qq \
    && apt-get upgrade \
      --yes -qq --no-install-recommends \
    && apt-get install \
      --yes -qq --no-install-recommends \
      build-essential \
      ca-certificates \
      libldap-dev \
      libpq-dev \
      libsasl2-dev \
      libssl-dev \
      libxml2-dev \
      libxmlsec1 \
      libxmlsec1-dev \
      libxmlsec1-openssl \
      libxslt-dev \
      pkg-config \
      python3-dev \
      python3-pip \
      python3-venv \
    && python3 -m venv /opt/netbox/venv \
    && /opt/netbox/venv/bin/python3 -m pip install --upgrade \
      pip \
      setuptools \
      wheel

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qq \
    && apt-get upgrade \
      --yes -qq --no-install-recommends \
    && apt-get install \
      --yes -qq --no-install-recommends \
      bzip2 \
      ca-certificates \
      curl \
      gdb \
      git \
      vim \
      sudo \
      libldap-common \
      libpq5 \
      ansible \
      nginx \
      libxmlsec1-openssl \
      openssl \
      openssh-server \
      supervisor \
      uuid-runtime \
      python3 \
      python3-distutils \
      tini \
    && curl --silent --output /usr/share/keyrings/nginx-keyring.gpg \
      https://unit.nginx.org/keys/nginx-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ lunar unit" \
      > /etc/apt/sources.list.d/unit.list \
    && apt-get update -qq \
    && apt-get install \
      --yes -qq --no-install-recommends \
      unit=1.31.1-1~lunar \
      unit-python3.11=1.31.1-1~lunar \
    && rm -rf /etc/update-motd.d \
    && rm -f /var/run/motd.dynamic \
    && rm -rf /var/lib/apt/lists/*


# Configure SSHD.
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN mkdir /var/run/sshd
RUN bash -c 'install -m755 <(printf "#!/bin/sh\nexit 0") /usr/sbin/policy-rc.d'
RUN ex +'%s/^#\zeListenAddress/\1/g' -scwq /etc/ssh/sshd_config
RUN ex +'%s/^#\zeHostKey .*ssh_host_.*_key/\1/g' -scwq /etc/ssh/sshd_config
RUN RUNLEVEL=1 dpkg-reconfigure openssh-server
RUN ssh-keygen -A -v
RUN update-rc.d ssh defaults
ADD etc /etc

# Configure sudo.
RUN ex +"%s/^%sudo.*$/%sudo ALL=(ALL:ALL) NOPASSWD:ALL/g" -scwq! /etc/sudoers

# Create a user 'itsupp'
RUN groupadd -g 1200 itsupp
RUN useradd -m -u 1200 -g 1200  -s /bin/bash itsupp
RUN usermod -aG sudo itsupp && echo "itsupp ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/itsupp
RUN chmod 0440 /etc/sudoers.d/itsupp 

RUN mv /etc/mysol /usr/bin/
RUN mv /etc/docker-entrypoint.sh /usr/bin/

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN echo 'itsupp:sunva11ey' | chpasswd

# Docker config
EXPOSE 22 80
ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
