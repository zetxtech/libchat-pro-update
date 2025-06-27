ARG VERSION
ARG BASE_IMAGE=fastgpt-pro
FROM ghcr.io/labring/${BASE_IMAGE}:${VERSION}

WORKDIR /app

# Copy the public key
COPY keys/public.pem /tmp/public.pem

# Switch to root for package installation
USER root

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
    find . -depth -name "*fastgpt*" -exec bash -c 'mv "$0" "${0//fastgpt/libchat}"' {} \; && \
    find . -depth -name "*FastGPT*" -exec bash -c 'mv "$0" "${0//FastGPT/LibChat}"' {} \; && \
    find . -depth -name "*FASTGPT*" -exec bash -c 'mv "$0" "${0//FASTGPT/LIBCHAT}"' {} \;

# Start
USER nextjs
ENV serverPath=./projects/app/server.js
ENTRYPOINT ["sh","-c","node ${serverPath}"]
