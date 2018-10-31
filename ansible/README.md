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

To run the playbook, do the following:

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

