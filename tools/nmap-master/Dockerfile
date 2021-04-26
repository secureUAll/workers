COPY ["/", "/nmap"]


ENV  PATH=${PATH}:/nmap

RUN echo "Configuring nnap" \

    && ./configure \

    && make \

    && sudo make install

ENTRYPOINT ["nmap"]

