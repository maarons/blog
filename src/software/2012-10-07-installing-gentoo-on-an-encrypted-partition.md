Title: Installing Gentoo on an encrypted partition
Date: 2012-10-07 09:09
Tags: cryptsetup, luks, gentoo

I have meant to do this for a long time but never really got around it.  Finally
today I decided to go for it and try to install Gentoo on a LUKS encrypted
partition.

Set‐up basics:

* Unencrypted boot partition — you can always put it on a flash drive if you
  want your computer to be fully encrypted.
* Single encrypted root partition — it is possible to have more partitions, but
  I didn’t bother.
* Encrypted swap.
* Normal partitions, no LVM witchcraft.

Most of the time you just have to follow the [Gentoo Handbook][handbook], the
only difference being that you should install on a LUKS device instead of an
unencrypted partition so I won’t reinvent the wheel and describe all the
details.  Formatting LUKS drives is also well documented so I’ll just skip to
the more challenging part — booting the system after the system is installed.

I’ll be using genkernel, so first it should be installed:

    USE="cryptsetup" emerge genkernel

Genkernel can not put cryptsetup into the initrd unless it is linked statically:

    USE="static" emerge cryptsetup

This will probably require some other packages to be recompiled with the
`static-libs` flag.

Now it is time to configure the kernel, go to `/usr/src/linux` and invoke
genkernel:

    genkernel --menuconfig --luks all

Depending on your hardware you might need more tweaks but I only had to touch
these options:

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
number and the disc/partition numbers):

    menuentry "Gentoo GNU+Linux 3.6.0" {
      set root='(hd0,msdos1)'
      linux /boot/kernel-genkernel-x86_64-3.6.0-gentoo rootfstype=ext4 crypt_root=/dev/sda4 real_root=/dev/mapper/root ro
      initrd /boot/initramfs-genkernel-x86_64-3.6.0-gentoo
    }

Now run:

    grub2-mkconfig -o /boot/grub2/grub.cfg

And install Grub with:

    grub2-install /dev/sda

You should be able to boot now=)

To make it complete you should also encrypt swap.  To do so edit
`/etc/conf.d/dmcrypt`, uncomment the lines about swap and run `rc-update add
dmcrypt boot`.  If you did put some stuff on separate encrypted partitions you
can tell Gentoo to unlock those partitions in `/etc/conf.d/dmcrypt` as well.

[handbook]: http://www.gentoo.org/doc/en/handbook/
