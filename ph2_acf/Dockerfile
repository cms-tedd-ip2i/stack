# Use AlmaLinux 9 as the base image
FROM almalinux:9

# Set environment variables
ENV PH2_ACF_VERSION=v6-25
ENV LD_LIBRARY_PATH=/opt/cactus/lib:$LD_LIBRARY_PATH
ENV PATH=/opt/cactus/bin:$PATH

# Install dnf-plugins-core for config-manager
RUN dnf install -y dnf-plugins-core && \
    dnf config-manager --set-enabled crb && \
    dnf install -y epel-release && \
    rm -rf /var/cache/dnf

# Update and install basic dependencies
RUN dnf update -y && \
    dnf install -y boost-devel pugixml-devel json-devel \
    bzip2-devel xz-devel zlib-devel libzstd-devel \
    git wget tar gzip make gcc gcc-c++ cmake \
    python3 python3-devel python3-pip \
    unzip which sudo git-extras clang-tools-extra \
    libusb-devel xorg-x11-xauth.x86_64 && \
    rm -rf /var/cache/dnf

# Add Erlang repository and install Erlang using RabbitMQ's official script
RUN curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | bash && \
    dnf install -y erlang && \
    rm -rf /var/cache/dnf

# Disable GPG check for rabbitmq_erlang to avoid conflicts
RUN sed -i 's/gpgcheck=1/gpgcheck=0/' /etc/yum.repos.d/rabbitmq_erlang.repo

# Install Protocol Buffers
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protobuf-all-3.19.4.tar.gz && \
    tar zxvf protobuf-all-3.19.4.tar.gz && \
    cd protobuf-3.19.4 && \
    ./configure && \
    make -j$(nproc) && \
    make check -j$(nproc) && \
    make install && \
    ldconfig && \
    pip3 install protobuf==3.19.4 && \
    rm -rf /protobuf-3.19.4

# Install uhal and controlhub with custom cache directory
RUN curl https://ipbus.web.cern.ch/doc/user/html/_downloads/ipbus-sw.repo -o /etc/yum.repos.d/ipbus-sw.repo && \
    dnf clean all && \
    dnf --setopt=cachedir=/tmp/dnf-cache makecache && \
    dnf --setopt=cachedir=/tmp/dnf-cache groupinstall -y uhal controlhub && \
    rm -rf /var/cache/dnf /tmp/dnf-cache

# Install ROOT
RUN dnf install -y root root-net-http root-net-httpsniff root-graf3d-gl \
    root-physics root-montecarlo-eg root-graf3d-eve root-geom && \
    rm -rf /var/cache/dnf

# Install gcc-toolset-12
RUN dnf install -y gcc-toolset-12 && \
    rm -rf /var/cache/dnf

# Install pybind11
WORKDIR /tmp
RUN wget https://github.com/pybind/pybind11/archive/refs/tags/v2.9.2.tar.gz && \
    tar zxvf v2.9.2.tar.gz && \
    rm v2.9.2.tar.gz

# Install Git LFS
RUN dnf install -y git-lfs && \
    git lfs install && \
    rm -rf /var/cache/dnf

# Clone and install Ph2_ACF
WORKDIR /opt
RUN git clone --recurse-submodules https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF.git
WORKDIR /opt/Ph2_ACF
RUN git checkout -b ${PH2_ACF_VERSION} ${PH2_ACF_VERSION}
WORKDIR /opt/Ph2_ACF
RUN /bin/bash -c ". ./setup.sh && \
    mkdir -p build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    rm -rf /var/cache/dnf"

# Set environment variables
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PATH=/usr/local/bin:$PATH

RUN dnf install -y mosquitto
RUN dnf install -y python3 python3-pip && \
    pip3 install paho-mqtt

COPY ph2_acf /opt/
# Add a startup script to set environment variables and start ControlHub
COPY start_container.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start_container.sh
RUN chmod +x /opt/run_ph2_acf.sh
#CMD ["/usr/local/bin/start_container.sh"]
# Set entrypoint to run the wrapper script
ENTRYPOINT ["/opt/run_ph2_acf.sh"]