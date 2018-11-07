This document outlines how installing mediawiki farm and multiple
wikis on a development machine has been accomplished.

# Steps:

1. Create base dirs

    ```
    mkdir -p ~/ots/mediawiki/opt
    mkdir -p ~/ots/mediawiki/etc
    mkdir -p ~/ots/mediawiki/etc/mediawiki
    mkdir -p ~/ots/mediawiki/etc/mediawiki/conf
    ```

1. Get MediaWiki/MediaWikiFarm source

    ```
    cd ~/ots/mediawiki/opt/
    git clone https://gerrit.wikimedia.org/r/mediawiki/extensions/MediaWikiFarm mediawikifarm
    cd ~/ots/mediawiki/opt
    wget https://releases.wikimedia.org/mediawiki/1.28/mediawiki-1.28.2.tar.gz
    tar zxf mediawiki-1.28.2.tar.gz
    mv mediawiki-1.28.2 1.28.2
    ```

1. Install MW/MWF

    ```
    cd ~/ots/mediawiki/opt/1.28.2/
    composer install --no-dev
    cd ~/ots/mediawiki/opt/mediawikifarm/
    composer install --no-dev
    ```

1. Create DBs

    In mysql
    ```
    CREATE DATABASE mw_test1;
    CREATE DATABASE mw_test2;
    ```

1. Add domain resolutions, choose one of the following:

   1. Add to hosts file
      ```
      #As root
      cat << EOF >> /etc/hosts
      127.0.0.1 otswiki.net test1.otswiki.net test2.otswiki.net
      EOF
      ```
   1. Set up [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html).
      * Add `address=/.otswiki.net/127.0.0.1` to `/etc/dnsmasq.conf` or wherever
        your dnsmasq file lives
      * Add `nameserver 127.0.0.1` to `/etc/resolv.conf`

1. Setup www directory

   ```
   ln -s ~/ots/mediawiki/opt/mediawikifarm/www /var/www/otswiki.net
   ```

1. Setup apache configuration

   Add the folowing to your apache config and restart apache
   ```
   <VirtualHost otswiki.net:80>
     ServerName otswiki.net
     ServerAlias *.otswiki.net
     DocumentRoot "/var/www/otswiki.net/"
     DirectoryIndex index.php
     <Directory "/var/www/otswiki.net/">
       Order allow,deny
       Allow from all
     </Directory>
     <FilesMatch "\.(cgi|shtml|phtml|php)$">
       SSLOptions +StdEnvVars
     </FilesMatch>
   </VirtualHost>
   ```

1. Setup MediaWikiFarmDirectories.php configuration

    ```
    cp  ~/ots/mediawiki/opt/mediawikifarm/docs/config/MediaWikiFarmDirectories.php ~/ots/mediawiki/opt/mediawikifarm/config/
    ```

1. Update configuration for use in home directory

    Change `~/ots/mediawiki/opt/mediawikifarm/config/MediaWikiFarmDirectories.php`
    * $wgMediaWikiFarmConfigDir -> '~/ots/mediawiki/etc/mediawiki';

1. Setup farms.yml

    Add the file `~/ots/mediawiki/etc/mediawiki/farms.yml`
    ```
    myfarm:
      server: '(?<wiki>[a-z0-9]+)\.otswiki\.net'
      variables:
        - variable: 'wiki'
      suffix: '$wiki'
      wikiID: '$wiki'
      versions: 'versions.yml'
      config:
        - file: 'conf/$wiki.yml'
          key: '$wiki'
    ```
1. Setup versions.yml

    Add the file `~/ots/mediawiki/etc/mediawiki/versions.yml`
    ```
    test1: 1.28.2
    test2: 1.28.2
    ```

1. Add mw test yml files

    Add `~/ots/mediawiki/etc/mediawiki/conf/test1.yml`
    ```
    wgDBtype: 'mysql'
    wgDBserver: 'localhost'
    wgDBname: 'mw_test1'
    wgDBuser: 'root'
    wgScriptPath: ''
    wgUseSkinVector: true
    ```
    Add `~/ots/mediawiki/etc/mediawiki/conf/test2.yml`
    ```
    wgDBtype: 'mysql'
    wgDBserver: 'localhost'
    wgDBname: 'mw_test2'
    wgDBuser: 'root'
    wgScriptPath: ''
    wgUseSkinVector: true
    ```

1. Initialize wikis

    ```
    cd ~/ots/mediawiki/opt/
    php 1.28.2/maintenance/install.php --confpath=/dev/null --dbtype=mysql --dbserver=localhost --dbuser=root --dbname=mw_test1 --lang=en --pass=mdpwiki "Wiki Test 1" "test"
    php 1.28.2/maintenance/install.php --confpath=/dev/null --dbtype=mysql --dbserver=localhost --dbuser=root --dbname=mw_test2 --lang=en --pass=mdpwiki "Wiki Test 2" "test"
    ```

1. Go to them in browser

    The sites `test1.otswiki.net` and `test2.otswiki.net` should be running mediawikis!

# Script to add wikis

If you have wildcard domain resolution, the farm set up, and apache routing
finished, you can add a new wiki via the following script.  It does minimal
error checking, so you need to make sure you name the wiki a valid hostname.

The wiki db needs to be passed in, and ideally unique from the WIKINAME, because
renaming databases is challenging, so we want to be able to rename the wiki while
keeping the database name the same.  We achieve this by linking the db name
with the id in the librehq_wikis database maintained by librehq.

```bash
#!/bin/bash

[ -z "$2" ] && echo "Need at least 2 arguments, the wiki name, and a db id" && exit

WIKINAME=$1
WIKIDB=$2

echo "CREATE DATABASE $WIKIDB" | mysql -uroot

if ! grep "^$WIKINAME: 1.28.2$" ~/ots/mediawiki/etc/mediawiki/versions.yml &> /dev/null ; then
    echo "$WIKINAME: 1.28.2" >> ~/ots/mediawiki/etc/mediawiki/versions.yml
fi

cat > ~/ots/mediawiki/etc/mediawiki/conf/$WIKINAME.yml << EOF
wgDBtype: 'mysql'
wgDBserver: 'localhost'
wgDBname: '$WIKIDB'
wgDBuser: 'root'
wgScriptPath: ''
wgUseSkinVector: true
EOF

# This creates the wiki with the admin user: test / mdpwiki
cd ~/ots/mediawiki/opt/
php 1.28.2/maintenance/install.php \
  --confpath=/dev/null \
  --dbtype=mysql \
  --dbserver=localhost \
  --dbuser=root \
  --dbname=$WIKIDB \
  --lang=en \
  --pass=mdpwiki8chars \
  "Wiki $WIKINAME" \
  "test"
```

# Script to rename a wiki

This is a bare bones way to change the name of the wiki according to MediaWiki.
While the wiki name is taken as a parameter in the addWiki.sh, it seems to not
be used in the mediawiki database anywhere, so that doesn't need updating.

```bash
#!/bin/bash

[ -z "$2" ] && echo "Need at least 2 arguments, the old wiki name, and new wiki name" && exit

WIKINAME_OLD=$1
WIKINAME_NEW=$2

sed -i -e "s/^$WIKINAME_OLD: 1.28.2$/$WIKINAME_NEW: 1.28.2/" ~/ots/mediawiki/etc/mediawiki/versions.yml
mv ~/ots/mediawiki/etc/mediawiki/conf/$WIKINAME_OLD.yml ~/ots/mediawiki/etc/mediawiki/conf/$WIKINAME_NEW.yml
```
