# Ansible Android Termux

Use Ansible to setup Termux on Android.

## Initial setup for Ansible

Allow access to internal storage: `termux-setup-storage`

Install pkgs: `pkg install openssh python`

Start sshd service: `sshd`

Import ssh public key from github/launchpad:

    pip install ssh-import-id
    ssh-import-id gh:$GITHUB_USERNAME
    ssh-import-id lp:$LAUNCHPAD_USERNAME

Now you should be able to access your device with ssh:

    ssh -i /path/to/ssh/pubkey -p 8022 $IP

In Ansible inventory `hosts.ini`:

    [termux]
    mi10     ansible_host=10.0.0.5
    oneplus8 ansible_host=10.0.0.6

    [termux:vars]
    ansible_ssh_port=8022
    ansible_python_interpreter=/data/data/com.termux/files/usr/bin/python

Now you should be able to run Ansible Playbook on your device:

    ./main.yaml -v

## share url to Termux

On Android, when you share url to Termux, `bin/termux-url-opener` will be called.
It is a python3 script which can handle different urls:

- YouTube: download video with `youtube-dl`, save to Video dir.
- YouTube Music: download `bestaudio` with `youtube-dl`, convert to mp3 with `ffmpeg`, save to Music dir.
- Google Play app url: download apk with `gplaycli`, save to Download dir.

More handlers to be added.
