Title: Installing Gentoo on an encrypted partition
Date: 2012-10-07 09:09
Tags: cryptsetup, luks, gentoo

I have meant to do this for a long time but never really got around it.  Finally
today I decided to go for it and try to install Gentoo on a LUKS encrypted
partition.

# Set‐up basics

* Unencrypted boot partition on a flash drive.
* Root partition protected with a key also found on the aforementioned flash
  drive.
* Encrypted swap that can be used for hibernating the system.
* Chain decryption of other partitions after root has been unlocked.
* Normal partitions, no LVM witchcraft.

# Installing the base system

Most of the time you just have to follow the [Gentoo Handbook][handbook].  Up
until the part where you compile the kernel the only difference is that the
root partition and swap are LUKS encrypted.  If you don’t know how to format
and mount LUKS drives you can look at the [archlinux wiki][arch-luks].

## Key file

You have to generate a key file that will be used to unlock the root partition
and swap.  It can take a while so in the meantime you can continue with the
installation.

    dd if=/dev/random of=keyfile bs=1 count=4096
    cryptsetup luksAddKey /dev/ROOT keyfile
    cryptsetup luksAddKey /dev/SWAP keyfile
    # You might want to remove other keys/passwords now.
    gpg --symmetric keyfile # Add a password to the key file.
    rm keyfile
    mv keyfile.gpg /media/FLASHDRIVE

## fstab

    # /boot is on a removable drive, you have to use UUID to reliably reference
    # it.  noauto means that you will be able to safely remove the pendrive
    # after boot.
    UUID=a5d4a6fc-c4af-4c7d-b39c-c6d65b2015c7 /boot ext4 noauto,noatime 1 2
    /dev/mapper/root                          /     ext4 noatime        0 1
    /dev/mapper/swap                          none  swap sw             0 0

## Configuring the kernel

You should install your favourite kernel sources (Gentoo sources recommended)
and update the `/usr/src/linux` symlink using `eselect kernel`.  To compile the
kernel and prepare an initrd I’ll be using genkernel, so first it should be
installed:

    USE="cryptsetup crypt" emerge genkernel

Genkernel can not put cryptsetup into the initrd unless it is linked statically:

    USE="static" emerge cryptsetup

This will probably require some other packages to be recompiled with the
`static-libs` flag.

Now it is time to configure the kernel, go to `/usr/src/linux` and invoke
genkernel:

    genkernel --menuconfig --luks --gpg all

Depending on your hardware you might need more tweaks but I only had to touch
these options (`=sys-kernel/gentoo-sources-3.6.0` and
`=sys-kernel/genkernel-3.4.43`):

    Device Drivers
      Multiple devices driver support (RAID and LVM)
         Device mapper support --> Y
           Crypt target support --> Y

    Cryptographic API
      SHA224 and SHA256 digest algorithm --> Y
      AES cipher algorithms --> Y

Truth be told I’m not really certain these options can’t be compiled as modules
but I’ve added them to the monolithic kernel just in case.

Also make sure your graphics drivers are included — genkernel often adds them as
modules which, at least for older Intel cards, means blinking and resolution
changing in the middle of the boot sequence.

When genkernel finishes the only thing left is the bootloader, I’ve used Grub 2
but Grub 1 or even LILO should do just fine.  Edit the `/etc/grub.d/40_custom`
file and add the following entry (of course you should edit the kernel version
number and partition identifiers):

    menuentry "Gentoo GNU+Linux 3.6.0" {
        search --no-floppy --fs-uuid --set=root a5d4a6fc-c4af-4c7d-b39c-c6d65b2015c7
        linux /boot/kernel-genkernel-x86_64-3.6.0-gentoo \
            rootfstype=ext4 \
            crypt_root=UUID=23cba145-7dad-4b14-9e2a-5e59644871aa \
            real_root=/dev/mapper/root \
            root_keydev=UUID=a5d4a6fc-c4af-4c7d-b39c-c6d65b2015c7 \
            root_key=keyfile.gpg \
            root_trim=yes \
            crypt_swap=UUID=2e711b6b-9406-486a-8cb9-47cb286290b7 \
            real_resume=/dev/mapper/swap \
            swap_keydev=UUID=a5d4a6fc-c4af-4c7d-b39c-c6d65b2015c7 \
            swap_key=keyfile.gpg \
            swap_trim=yes \
            ro
        initrd /boot/initramfs-genkernel-x86_64-3.6.0-gentoo
    }

WARNING: At the time of writing genkernel doesn’t support UUID matching for
`*_keydev`, you’ll need [this patch][uuid-patch] to make it work.

UPDATE: This was merged into genkernel 3.4.45 — you don’t need to do anything
extra to get the cool UUID matching.

Now run:

    grub2-mkconfig -o /boot/grub2/grub.cfg

And install Grub with:

    grub2-install /dev/FLASHDRIVE

You should be able to boot now=)

If you want to use more encrypted partitions you can put their keyfiles on the
root partition and then configure them in `/etc/conf.d/dmcrypt` to automatically
decrypt them on boot.

[handbook]: http://www.gentoo.org/doc/en/handbook/
[arch-luks]: https://wiki.archlinux.org/index.php/Dm-crypt_with_LUKS
[uuid-patch]: https://bugs.gentoo.org/show_bug.cgi?id=378105
