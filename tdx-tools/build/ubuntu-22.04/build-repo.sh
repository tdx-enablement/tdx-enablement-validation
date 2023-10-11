#!/bin/bash

set -ex
set -o pipefail

THIS_DIR=$(dirname "$(readlink -f "$0")")
GUEST_REPO="guest_repo"
HOST_REPO="host_repo"
STATUS_DIR="${THIS_DIR}/build-status"
LOG_DIR="${THIS_DIR}/build-logs"

export DEBIAN_FRONTEND=noninteractive

GUEST_DEFAULT_PKG=" \
shim_*_amd64.deb \
grub-efi-amd64_*_amd64.deb grub-efi-amd64-bin_*_amd64.deb \
linux-image-unsigned-6.2.16-*.deb linux-headers-6.2.16-* linux-modules-6.2.16-* \
"

HOST_DEFAULT_PKG=" \
linux-image-unsigned-6.2.16-*.deb linux-headers-6.2.16-* linux-modules-6.2.16-* linux-modules-extra-6.2.16-* \
qemu-system-x86_7.2*.deb qemu-system-common_7.2*.deb qemu-system-data_7.2*.deb \
ovmf_*_all.deb \
libvirt-clients_*.deb libvirt0_*.deb libvirt-daemon_*.deb libvirt-daemon-system_*.deb libvirt-daemon-system-systemd_*.deb\
 libvirt-daemon-driver-qemu_*.deb libvirt-daemon-config-network_*.deb libvirt-daemon-config-nwfilter_*.deb\
 libvirt-login-shell_*.deb libvirt-daemon-driver-lxc_*.deb libvirt-dev_*.deb \
td-migration_*_amd64.deb \
vtpm-td_*_amd64.deb \
"

build_check() {
    sudo apt update

    if ! command -v "dpkg-scanpackages"
    then
        sudo apt install dpkg-dev -y
    fi

    [[ -d "$LOG_DIR" ]] || mkdir "$LOG_DIR"
    [[ -d "$STATUS_DIR" ]] || mkdir "$STATUS_DIR"
    if [[ "$1" == clean-build ]]; then
        rm -rf "${STATUS_DIR:?}"/*
    fi

    if [[ ! -z ${rust_mirror} ]]; then
        mkdir -p ~/.cargo
        cat > ~/.cargo/config << EOL
[source.crates-io]
replace-with = 'mirror'

[source.mirror]
registry = "${rust_mirror}"

[registries.mirror]
index = "${rust_mirror}"
EOL
    fi

    if [[ ! -z ${rustup_dist_server} ]]; then
        export RUSTUP_DIST_SERVER="${rustup_dist_server}"
    fi
    if [[ ! -z ${rustup_update_server} ]]; then
        export RUSTUP_UPDATE_SERVER="${rustup_update_server}"
    fi
}

build_kernel () {
    pushd intel-mvp-tdx-kernel
    [[ -f $STATUS_DIR/kernel.done ]] || ./build.sh 2>&1 | tee "$LOG_DIR"/kernel.log
    touch "$STATUS_DIR"/kernel.done
    popd
}

build_qemu () {
    pushd intel-mvp-tdx-qemu-kvm
    [[ -f $STATUS_DIR/qemu.done ]] || ./build.sh 2>&1 | tee "$LOG_DIR"/qemu.log
    touch "$STATUS_DIR"/qemu.done
    popd
}

build_tdvf () {
    pushd intel-mvp-ovmf
    [[ -f $STATUS_DIR/ovmf.done ]] || ./build.sh 2>&1 | tee "$LOG_DIR"/ovmf.log
    touch "$STATUS_DIR"/ovmf.done
    popd
}

build_libvirt () {
    pushd intel-mvp-tdx-libvirt
    [[ -f $STATUS_DIR/libvirt.done ]] || ./build.sh 2>&1 | tee "$LOG_DIR"/libvirt.log
    touch "$STATUS_DIR"/libvirt.done
    popd
}

build_migtd () {
    pushd intel-mvp-tdx-migration
    [[ -f $STATUS_DIR/migtd.done ]] || ./build.sh 2>&1 | tee "$LOG_DIR"/migtd.log
    touch "$STATUS_DIR"/migtd.done
    popd
}

build_vtpm-td () {
    pushd intel-mvp-vtpm-td
    [[ -f $STATUS_DIR/vtpm-td.done ]] || ./build.sh 2>&1 | tee "$LOG_DIR"/vtpm-td.log
    touch "$STATUS_DIR"/vtpm-td.done
    popd
}

_build_repo() {
    PKG_DIR=$1
    if [ -d jammy ]; then
        rm -rf jammy
    fi

    if [ -d mini-dinstall ]; then
        rm -rf mini-dinstall
    fi

    mkdir -p mini-dinstall

    mv $PKG_DIR ./mini-dinstall/incoming
    cur=$(realpath .)

    content='[DEFAULT] 
archive_style = simple-subdir
archivedir = '$cur'
architectures = all, amd64
dynamic_reindex = 1
verify_sigs = 0
incoming_permissions = 0775
generate_release = 1
mail_on_success = false
release_description = Linux MVP Stacks Packages for Ubuntu
[jammy]'

    echo "$content" > ./mini-dinstall/mini-dinstall.conf

    mini-dinstall -b -q -c ./mini-dinstall/mini-dinstall.conf

    rm -rf mini-dinstall
}

_build_guest_repo() {
    mkdir -p $GUEST_REPO/incoming

    pushd intel-mvp-tdx-kernel
    cp *.build *.buildinfo *.changes *.tar.gz *.deb ../$GUEST_REPO/incoming/
    popd

    pushd $GUEST_REPO

    _build_repo ./incoming

    popd
}

_build_host_repo () {
    mkdir -p $HOST_REPO/incoming

    pushd intel-mvp-tdx-kernel
    cp *.build *.buildinfo *.changes *.tar.gz *.deb ../$HOST_REPO/incoming/
    popd    

    pushd intel-mvp-tdx-qemu-kvm
    cp *.build *.buildinfo *.changes *.deb *.ddeb ../$HOST_REPO/incoming/
    popd

    pushd intel-mvp-ovmf
    cp *.build *.buildinfo *.changes *.deb ../$HOST_REPO/incoming/
    popd    

    pushd intel-mvp-tdx-libvirt
    cp *.build *.buildinfo *.changes *.tar.xz *.deb *.ddeb ../$HOST_REPO/incoming/
    popd

    pushd intel-mvp-tdx-migration
    cp *.build *.buildinfo *.changes *.deb ../$HOST_REPO/incoming/
    popd

    pushd intel-mvp-vtpm-td
    cp *.build *.buildinfo *.changes *.deb  ../$HOST_REPO/incoming/
    popd

    pushd $HOST_REPO
    _build_repo ./incoming
    popd
}

build_repo () {
    _build_guest_repo
    _build_host_repo
}



build_check "$1"

pushd "$THIS_DIR"

build_kernel
build_qemu
build_tdvf
build_libvirt
build_migtd
build_vtpm-td

build_repo

popd
