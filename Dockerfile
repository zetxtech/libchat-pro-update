ARG VERSION=latest
ARG BASE_IMAGE=fastgpt-pro

# Stage 1: Base image stage
FROM ghcr.io/labring/${BASE_IMAGE}:${VERSION} AS base_image

# Stage 2: Patching stage
FROM python:3.9-alpine AS patcher

WORKDIR /patch

# Copy the patching script and public key
COPY patch.py .
COPY keys/public.pem /tmp/public.pem

# Copy the entire app directory to be patched
COPY --from=base_image /app /app

# Make the script executable
RUN chmod +x patch.py

# Run the patching script on the entire app directory
RUN python patch.py /app

# Stage 3: Final stage
FROM ghcr.io/labring/${BASE_IMAGE}:${VERSION}

WORKDIR /app

# Copy the entire patched app directory from the patcher stage
COPY --from=patcher /app ./

# Start
USER nextjs
ENV serverPath=./projects/app/server.js
ENTRYPOINT ["sh","-c","node ${serverPath}"]
