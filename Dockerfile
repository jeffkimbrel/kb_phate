FROM kbase/sdkbase2:python
MAINTAINER kimbrel1@llnl.gov
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update

RUN \
  apt-get update && \
  apt-get install -y gcc && \
  apt-get install wget

RUN wget http://lowelab.ucsc.edu/software/tRNAscan-SE.tar.gz \
  && tar -xvf tRNAscan-SE.tar.gz \
  && cd tRNAscan-SE-1.3.1 \
  && make \
  && make install

RUN \
  git clone https://github.com/deprekate/fastpath.git && \
  cd fastpath && \
  make

RUN \
  git clone --recursive https://github.com/deprekate/PHANOTATE.git && \
  cd PHANOTATE && \
  make

ENV PATH=$PATH:/root/bin

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
