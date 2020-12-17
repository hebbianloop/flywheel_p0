# flywheel_p0

# Use brats docker image
FROM nipype/nipype:latest

USER root

LABEL MAINTAINER="Shady El Damaty <eldamaty.shady@gmail.com>"

# Install packages
RUN apt-get update \
    && apt-get install -y \
    bsdtar \
    zip \
    unzip \
    gzip 

RUN pip install --upgrade pip && \
    pip install flywheel-sdk


# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}


# useful snippet :: Save docker environ
#RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); #json.dump(dict(os.environ), f)'

# Copy external requirements
COPY manifest.json ${FLYWHEEL}/
COPY run.py ${FLYWHEEL}/

# Configure entrypoint
RUN chmod a+x ${FLYWHEEL}/run.py
ENTRYPOINT ["${FLYWHEEL}/run.py"]