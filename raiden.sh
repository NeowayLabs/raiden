#!/bin/bash

set -o nounset

if (( $# < 2 )); then
    echo "usage: "$0" <RAID chunk size in kb> <ext4|xfs>"
    echo "eg: "$0" 256"
    exit
fi

CHUNK_SIZE_KB=$1
FILESYSTEM=$2
BLOCK_SIZE_BYTES=4096
BLOCK_SIZE_KB=4
NUMBER_RAID_DISKS=8
RAID_DEVICE=/dev/md0
TEST_RUNTIME=120
DEVICES="
    /dev/sdc
    /dev/sdd
    /dev/sde
    /dev/sdf
    /dev/sdg
    /dev/sdh
    /dev/sdi
    /dev/sdj
"

echo "All data will be lost on configured devices, are you sure to go on ?"
read -p "Are you sure? " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then echo "aborting"
    exit 0
fi
echo

# Destroy previous RAID config
sudo umount /dev/md0
mdadm --manage --stop $RAID_DEVICE
mdadm --manage --remove $RAID_DEVICE

set -o errexit

echo
echo "RAID chunk size (KB): "$CHUNK_SIZE_KB
mdadm --create --force --verbose $RAID_DEVICE \
        --level=0 \
        --name=md0 \
        --chunk=$CHUNK_SIZE_KB"K" \
        --raid-devices=$NUMBER_RAID_DISKS $DEVICES

if [ "$FILESYSTEM" == "ext4" ]; then
    # https://wiki.archlinux.org/index.php/RAID#Calculating_the_Stride_and_Stripe_Width
    # stride = chunk size / block size
    # stripe width = number of data disks * stride
    stride=$(expr $CHUNK_SIZE_KB \/ $BLOCK_SIZE_KB)
    stripe_width=$(expr $NUMBER_RAID_DISKS \* $stride)

    echo "Formatting filesystem as ext4 with blocksize: "$BLOCK_SIZE_BYTES" stride: "$stride" stripe_width: "$stripe_width
    mkfs.ext4 -v -L pgdata -b $BLOCK_SIZE_BYTES -E stride=$stride,stripe-width=$stripe_width $RAID_DEVICE
fi

if [ "$FILESYSTEM" == "xfs" ]; then
    # xfs allows more than 4K
    # https://raid.wiki.kernel.org/index.php/RAID_setup#XFS
    echo "Formatting filesystem as xfs with blocksize: "$BLOCK_SIZE_BYTES
    mkfs.xfs -f -L pgdata -b size=$BLOCK_SIZE_BYTES -d su=$CHUNK_SIZE_KB"k" -d sw=$NUMBER_RAID_DISKS $RAID_DEVICE
fi

mkdir -p /fiotests
mount /dev/md0 /fiotests

olddir=$(pwd)
cd /fiotests

echo "Starting tests"

blocksizes="8K 16K 32K 64K 128K 256K 512K"
for blocksize in $blocksizes
do
    echo
    echo
    echo "========== starting tests with blocksize: "$blocksize" =========="
    echo
    echo "testing sequential write"
    fio --name fio_test_file --direct=1 --rw=write --bs=$blocksize --size=1G --numjobs=100 --time_based --runtime=$TEST_RUNTIME --group_reporting
    echo "testing sequential read"
    fio --name fio_test_file --direct=1 --rw=read --bs=$blocksize --size=1G --numjobs=100 --time_based --runtime=$TEST_RUNTIME --group_reporting
    echo "testing random write"
    fio --name fio_test_file --direct=1 --rw=randwrite --bs=$blocksize --size=1G --numjobs=100 --time_based --runtime=$TEST_RUNTIME --group_reporting
    echo "testing random read"
    fio --name fio_test_file --direct=1 --rw=randread --bs=$blocksize --size=1G --numjobs=100 --time_based --runtime=$TEST_RUNTIME --group_reporting
    echo
    echo "========== done =========="
    echo
done

cd $olddir
