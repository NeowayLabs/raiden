#!/bin/bash

CHUNK_SIZE_KB=512
BLOCK_SIZE_BYTES=4096
BLOCK_SIZE_KB=4
NUMBER_RAID_DISKS=17
DEVICES="
    /dev/sdc
    /dev/sdd
    /dev/sde
    /dev/sdf
    /dev/sdg
    /dev/sdh
    /dev/sdi
    /dev/sdj
    /dev/sdk
    /dev/sdl
    /dev/sdm
    /dev/sdn
    /dev/sdo
    /dev/sdp
    /dev/sdq
    /dev/sdr
    /dev/sds
"

echo "All data will be lost on configured devices, are you sure to go on ?"
read -p "Are you sure? " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "aborting"
    exit 0
fi

# create raid
# TODO: Destroy previous RAID config

mdadm --create --verbose /dev/md0 \
        --level=0 \
        --name=md0 \
        --chunk=CHUNK_SIZE_KB"K" \
        --raid-devices=$NUMBER_RAID_DISKS $DEVICES

# https://wiki.archlinux.org/index.php/RAID#Calculating_the_Stride_and_Stripe_Width
# stride = chunk size / block size
# stripe width = number of data disks * stride
stride=$($CHUNK_SIZE_KB \/ $BLOCK_SIZE_KB)
stripe_width=$(expr $NUMBER_RAID_DISKS \* $stride)

echo "Formatting filesystem as ext 4 with blocksize: "$blocksize" stride: "$stride" stripe_width: "$stripe_width

mkfs.ext4 -v -L pgdata -b $blocksize -E stride=$stride,stripe-width=$stripe_width /dev/md0
