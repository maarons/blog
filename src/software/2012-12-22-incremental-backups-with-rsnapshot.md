Title: Incremental backups with rsnapshot
Date: 2012-12-22 08:58
Tags: linux, backup

I’ve been putting this away for a very long time but it turns out that backups
don’t have to be hard.  With just a few lines of configuration you can get fast,
incremental backups of your system.

# Set‐up
I will assume that the backup drive is mounted in `/media/DRIVE`.

# Local system
Backing up your local system couldn’t be easier, just dump this into
`/etc/rsnapshot.conf`:

    config_version      1.2

    no_create_root      1

    cmd_rsync       /usr/bin/rsync
    cmd_ssh         /usr/bin/ssh
    cmd_rm          /bin/rm
    cmd_logger      /usr/bin/logger
    cmd_du          /usr/bin/du

    snapshot_root           /media/DRIVE/mysystem
    retain      manual      30
    backup      /           root/

    exclude     dev/
    exclude     media/
    exclude     mnt/
    exclude     proc/
    exclude     sys/
    exclude     tmp/

Create the target backup directory

    mkdir /media/DRIVE/mysystem

And you are all set — `rsnapshot manual` run as `root` will rotate previous
backups and create a new one.

Two important things:

* You have to use tabs in the configuration file, actual tab characters, not
  spaces.

* If you’ve set `no_create_root 1` in the config file you’ll have to create the
  backup directory manually — you can remove this line but then if you forget to
  mount your backup drive rsnapshot will just dump the backup in `/media` on
  your local drive.

# Remote system
This gets more tricky if you don’t want to allow `root` SSH login on the remote
machine.  This is what you have to do to prepare the remote machine:

* Create a user for running rsync, let’s call him `rsnap`.

* Put this in `~/.ssh/authorized_keys`:

    command="/home/rsnap/validate-rsync.sh" ssh-rsa SshKeyOfRootOntheLocalMachine

* Put this in `~/validate-rsync.sh`:

        #!/bin/bash
        case "$SSH_ORIGINAL_COMMAND" in
        *\&*|*\|*|*\;*|*\>*|*\<*|*\!*)
            # This is a suspicious command using some shell characters.
            exit 1
            ;;
        /usr/bin/rsync\ --server\ --sender\ *)
            sudo $SSH_ORIGINAL_COMMAND
            ;;
        *)
            exit 1
            ;;
        esac

* Make it executable.

        chmod +x ~/validate-rsync.sh

* Previous three steps will only allow rsync connections after password‐less SSH
  login.

* Allow `rsnap` to execute rsync as root without a password.  Use `visudo` for that.

        rsnap ALL=(root) NOPASSWD: /usr/bin/rsync

You are almost set, just change the `backup` line in `rsnapshot.conf` to `backup
rsnap@someip:/ root/`, add `rsync_long_args --rsync-path=/usr/bin/rsync` and
you’re done.

It was super easy wasn’t it?  Makes you wonder why you haven’t done this
earlier.
