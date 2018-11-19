# README

To run this playbook, you should have Ansible installed locally.  On a
Debian system, you can do this with:

    $ sudo apt-get install ansible

This will create a directory `/etc/ansible` and within that a file
`/etc/ansible/hosts`.  To run this playbook, you should add the
following lines to the `hosts` file:

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

However, you'll most likely need to encrypt some secrets.  For example,
in this playbook we encrypt the database password.

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
[documentation in another
branch](https://github.com/OpenTechStrategies/librehq-wikis/blob/mediawiki-updates/MEDIAWIKI_INSTALL.md)
of this repository.  We expect these to be united on the master branch
in the future.

To use the mediawiki farm parts of this Ansible playbook, you will need
to add the database password to `test1.yml` and `test2.yml`.

    $ cp mediawikifarmdocs/test1.yml.tmpl mediawikifarmdocs/test1.yml
    # Edit database password to match the one you entered in your vault


