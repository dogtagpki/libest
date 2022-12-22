#
# Copyright Red Hat, Inc.
#
# SPDX-License-Identifier: GPL-2.0-or-later
#

################################################################################
FROM registry.fedoraproject.org/fedora:latest AS libest-builder

# Install build tools
RUN dnf install -y dnf-plugins-core rpm-build

# Import libEST source
COPY . /root/libest/
WORKDIR /root/libest

# Create source tarball
RUN mkdir -p /root/rpmbuild/SOURCES
RUN tar czvf /root/rpmbuild/SOURCES/libest-3.2.0-pki.tar.gz \
    --transform "s,^./,libest-3.2.0-pki/," \
    --exclude .git \
    -C /root/libest \
    .

# Install build dependencies
RUN dnf builddep -y --spec libest.spec

# Build libEST packages
RUN rpmbuild -ba libest.spec

# Consolidate libEST packages
RUN mkdir -p /root/RPMS
RUN find /root/rpmbuild/RPMS -mindepth 2 -type f -exec mv {} /root/RPMS \;

################################################################################
FROM alpine:latest AS libest-dist

# Import libEST packages
COPY --from=libest-builder /root/RPMS /root/RPMS/
