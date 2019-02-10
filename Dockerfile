# Build with:
#     docker build --tag=tubedl .
#
# Run e.g. tests with:
#     docker run -it --rm tubedl /bin/sh -c 'tox'
#
# Or for interactive shell:
#     docker run -it --rm tubedl

FROM ubuntu:18.04

# configure locale
RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# RUN apt -y update -qq \
#     && apt -y install -qq --no-install-recommends curl unzip ca-certificates \
#     && apt -y autoremove

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

# install system dependencies
RUN apt -y install -qq --no-install-recommends \
        python3 virtualenv python3-pip sudo \
    && apt -y autoremove

# prepare non root env
RUN useradd --create-home --shell /bin/bash ${USER}

# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR ${WORK_DIR}
COPY --chown=user:user . ${WORK_DIR}
USER ${USER}

# setup virtualenv
RUN make virtualenv
