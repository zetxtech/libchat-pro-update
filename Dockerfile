ARG VERSION
FROM ghcr.io/labring/fastgpt-pro:${VERSION}

WORKDIR /app

# Copy the public key
COPY keys/public.pem /tmp/public.pem

# Install necessary tools
RUN apk add --no-cache \
    util-linux \
    && rm -rf /var/cache/apk/*

# Replace the public key in all files
RUN find ./projects/app/.next -type f -exec sh -c '\
    if grep -q "BEGIN PUBLIC KEY" "{}"; then \
        sed -i -e "/-----BEGIN PUBLIC KEY-----/,/-----END PUBLIC KEY-----/c\\$(sed -e "1h;2,\$H;\$!d;g" -e "s/\n/\\\\n/g" /tmp/public.pem)" "{}"; \
    fi' \;

# Replace text in all files
RUN find ./projects/app/.next -type f -exec sed -i 's/fastgpt/libchat/g; s/FastGPT/LibChat/g; s/FASTGPT/LIBCHAT/g' {} \;

# Rename files and directories containing the patterns
RUN cd ./projects/app/.next && \
    find . -depth -name "*fastgpt*" -execdir bash -c 'mv "$1" "${1//fastgpt/libchat}"' bash {} \; && \
    find . -depth -name "*FastGPT*" -execdir bash -c 'mv "$1" "${1//FastGPT/LibChat}"' bash {} \; && \
    find . -depth -name "*FASTGPT*" -execdir bash -c 'mv "$1" "${1//FASTGPT/LIBCHAT}"' bash {} \;

# Start
ENV serverPath=./projects/app/server.js
ENTRYPOINT ["sh","-c","node ${serverPath}"]
