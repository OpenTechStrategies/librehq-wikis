# README

## Install Ansible

To run this playbook, you should have Ansible installed locally.  On a
Debian system, you can do this with:

    $ sudo apt-get install ansible

## Hosts file

If you are doing local testing using Vagrant and VirtualBox, you can
skip ahead to the section about encrypting secrets.

Otherwise, you'll need to edit the `hosts` file. After installing
Ansible, it should be here: `/etc/ansible/hosts`. Add the following
lines to that file:

```
[mediawiki]
YOUR_SERVER_NAME_OR_IP_HERE
```

You may have as many hosts as you like within the `[mediawiki]` group.
You should have SSH access to those hosts.  You can test the connection
to them with `ansible mediawiki -u root -m ping`.  You should see
something like the following for each host in your `[mediawiki]` group:

```
example.com | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

## Running without secrets

To run the simplest version of the playbook, with no secrets, do the
following:

    $ cd /path/to/this/repository/ansible/
    $ ansible-playbook mediawiki-install.yml

You should see something like the following:

```
PLAY [mediawiki] ***************************************************************

TASK [Gathering Facts] *********************************************************
ok: [example.com]

TASK [install prerequisites] ***************************************************
ok: [example.com] => (item=apache2)
ok: [example.com] => (item=curl)
changed: [example.com] => (item=mariadb-server)
changed: [example.com] => (item=php)
changed: [example.com] => (item=php-apcu)
changed: [example.com] => (item=php-intl)

PLAY RECAP *********************************************************************
example.com : ok=2    changed=1    unreachable=0    failed=0   
```

## Encrypt secrets

Most likely, you'll need to encrypt some secrets.  For example, in this
playbook we encrypt the database password.

A best practice is to create an Ansible Vault file with all sensitive
variables and use `ansible-vault encrypt` to encrypt the file.  You can
use a plaintext (not encrypted) file to redirect to the vault file for
easier maintenance, as described in [the
documentation](https://docs.ansible.com/ansible/2.5/user_guide/playbooks_best_practices.html#best-practices-for-variables-and-vaults).
For this playbook, copy the example vault file and fill it in with your
own secrets, then vault encrypt it.

```
    $ cp ansible/mediawiki_vars/vault.yml.tmpl ansible/mediawiki_vars/vault.yml
    # Edit vault file and fill in your passwords
    # Encrypt the file
    $ ansible-vault encrypt mediawiki_vars/vault.yml
    New Vault password:
    Confirm New Vault password:

    Encryption successful
```

Then, when you run the playbook, you'll use the `--ask-vault-pass` flag.

    $ ansible-playbook mediawiki-install.yml --ask-vault-pass
    Vault password:

If you want to run the command in a script, you can also pass the vault
password in a file.

## Server configuration

We include an `mwiki-default.conf.tmpl` in this directory.  You will need to copy that to your .conf file like so:

    $ cp mwiki-default.conf.tmpl mwiki-default.conf
    # Edit ServerName to be whatever you want to call your host

If you know what changes you want to make to your Apache configuration
(e.g. adding SSL), you can make those here.  You will at least need
to fill in the Server Name.

## Mediawiki Farm (i.e., multiple wikis)

Our configuration for multiple wikis is currently closely based on
the documentation in
[MEDIAWIKI_INSTALL.md](https://github.com/OpenTechStrategies/librehq-wikis/blob/mvp-dev/MEDIAWIKI_INSTALL.md).

To use the mediawiki farm parts of this Ansible playbook, you will need
to add the database password to `test1.yml` and `test2.yml`.

    $ cp mediawikifarmdocs/test1.yml.tmpl mediawikifarmdocs/test1.yml
    # Edit database password to match the one you entered in your vault


## Local testing

Locally, Ansible works well with Vagrant.

    $ sudo apt-get install vagrant
    $ sudo apt-get install virtualbox

Note that the [Vagrant
documentation](https://www.vagrantup.com/docs/installation/) suggests
_not_ using the version of Vagrant packaged by your operating system,
but rather using the more complete and up-to-date versions they
[provide](https://www.vagrantup.com/downloads.html).

(2018/12/06: the version from the Vagrant website worked (2.2.2),
but the one provided by Ubuntu 18.04 did not (2.0.2).)

Either way, downloading may take a few minutes.  If you choose to
download the `.deb` file, you can install it with `sudo dpkg -i
/path/to/vagrant_2.2.1_x86_64.deb`. Test your local installation with
the following commands:

    # Adds a Debian image to your VirtualBox installation
    $ vagrant box add debian/testing64

    # Move to `vagrant` directory
    $ cd vagrant

    # Since there is a committed Vagrantfile in this repo, you don't
    # need to `vagrant init` and can instead move on to these commands:
    
    # Optional: edit the `config.vm.box` setting in the Vagrantfile,
    # it should already be set: config.vm.box = "debian/testing64"
    $ emacs Vagrantfile

    $ vagrant up

You may get a persistent error like `default: Warning: Authentication
failure. Retrying...`.  Check that the virtual machine is being created
correctly in VirtualBox (you can look in the GUI to see if it appears
and is running).  The quickest and simplest way to resolve this is by
copying [the Vagrant default key
files](https://github.com/hashicorp/vagrant/tree/master/keys) to your
`.ssh` directory (on your host machine, not the new virtual guest
machine).  The Vagrantfile assumes that this default private key is
present at `~/.ssh/vagrant-insecure`, as noted in the line
`config.ssh.private_key_path = "~/.ssh/vagrant-insecure"`. Make sure
the default key files end in a newline (see this [bug
report](https://github.com/hashicorp/vagrant/issues/10333)).

If you then SSH to your vagrant host __as `vagrant`__ with `vagrant
ssh`, you should be able to connect successfully.

Because the Mediawiki playbook is intended to be run as root, you should
copy the guest machine's `authorized_keys` file from the `vagrant` user
to `root`.  This will allow Vagrant and Ansible to access the guest
machine as root. (This is not a security best practice, but since this
virtual machine should only be used for local testing, it is an
acceptable risk.)

    $ vagrant ssh
    vagrant@testing$ sudo su
    root@testing$ cd ~
    root@testing$ mkdir .ssh
    root@testing$ cp /home/vagrant/.ssh/authorized_keys .ssh

Then disconnect from the guest machine (e.g. type `cmd-d`).  Open the
Vagrantfile and uncomment the line designating root as the username.

To run the Ansible file and set up Mediawiki on your local virtual
machine:

    $ vagrant provision

If you need to test a clean build, you can clear the Vagrant virtual
machine with `vagrant destroy`.  From there, just start again at
`vagrant up` above.

### Checking MediaWiki in a browser

To check the MediaWiki installation in a browser, edit the
Vagrantfile and uncomment this line to enable port forwarding,
(to forward a port on your host OS to a port on the guest VM):

    config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

You may also need to edit the Apache config file `000-default.conf`:

    $ vagrant ssh
    $ cd ../etc/apache2/sites_available/
    $ nano 000-default.conf

Then change the `DocumentRoot` to `/var/www/mediawiki/`, and restart
the VM:

    $ vagrant halt
    $ vagrant up

Now you should be able to see MediaWiki in your browser at
`localhost:8080`.
