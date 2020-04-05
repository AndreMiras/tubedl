# Build with:
#     docker build --tag=andremiras/tubedl .
#
# Run e.g. tests with:
#     docker run -it --rm andremiras/tubedl /bin/sh -c 'make test'
#
# Or for interactive shell:
#     docker run -it --rm andremiras/tubedl

FROM ubuntu:18.04

# configure locale
RUN apt update -qq > /dev/null && apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8

ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

# install system dependencies
RUN apt -y install -qq --no-install-recommends \
        ffmpeg make python3 python3-pip sudo virtualenv \
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
