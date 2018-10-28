# Initial Project Outline

## Step 1 - Single instance

1. Initial setup as submodule
   * flask import setup, installable python module setup
1. Initial setup as standalone
   * flask subproject set up, basic documentation
1. First csv2wiki page
   * This will consist of a single page with an upload box for a csv2wiki config file, and csv.  Both known to work
1. csv2wiki page runs against preconfigured mediawiki instance
   * Making the previous page work as it should.  The only time concern is if there's substantial changes needed to csv2wiki to have it running from inside another python instance

## Step 2 - Multi instance

1. Set up mediawiki multiple wiki instance
   * Some promising things at [https://www.mediawiki.org/wiki/Manual:Wiki_family] and [https://www.mediawiki.org/wiki/Extension:MediaWikiFarm]
   * Evaluate the options, choose one, attempt to implement it
1. csv2wiki page adds a wiki to the wiki family
   * This should go quickly after the former is set up correctly
   * Use a default username / pw for wiki instance (to be corrected in step 4)
1. csv2wiki allows configuration of wikis to be added
1. Access wikis through ```http://<site>/<wikiname>```
   * May be hard to make the routing happen just right

## Step 3 - Account federation - core only

This section intentionally left blank due to this step being core only

## Step 4 - Wiki maintenace

1. Add wiki control page as landing page after logins
   * Has the current add feature
   * Has a list of currently added wikis after adding
1. Add wiki rename
   * Unless mediawiki is hostile to renaming
1. Add wiki delete
   * Has double checking about dropping
   * No idea how one drops a wiki, so will need reserach
1. Setup wiki account upon creation
   * Take username / pw
1. Add system specificed plugins to wikis on setup
   * Might not be easy to do, if so, probably drop
   * Look at current csv2wiki install to see what kinds of plugins were needed

## Step 5 - Error checking

1. Wiki name error checking
   * Check wiki name already there from someone else, require unique
   * Check on renaming and adding
1. Wiki csv error checking
   * This is really unspecified, so we should note what kinds of errors we want to ping about

## Step 6 - Csv2Wiki upload specifications

** Circle back about how this config file page generator / displayer looks **

1. Add webpage that generates wiki config file
   * When uploading a csv to generate a wiki, allow a user to use a page to dynamically generate the config file
   * Allow them to download it for reuploads
   * If we want it to be a smart interface, this will take more time (smart meaning they can do a wysiwyg using the csv files headers), as opposed to having to use the ```{1}_{2}``` notation.
1. When wiki is generated, store config file to database
1. Allow users to review current config in edit page
   * When uploading both csv and config file, have them first be able to stop and edit the config file, and download the updated configuration
1. Allow xlsx
   * This should be a simple call to csvkit's in2csv
1. Allow configuration of csv parameters
   * Delimeter configuration

## Step 7 - ansible - core only

This section inentionally left blank due to this step being core only
