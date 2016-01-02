* 12/22/15: if you delete a node in the web interface, it'll be also deleted from the database; you can now configure in which interval the server is requesting the node configs;
    the size of the canvas part is now configurable; node reboot time is now adjustable
* 11/16/15: implemented a canvas fuzzer for 2D canvas elements
* 11/11/15: implemented the stats page in the web interface; this site lists the occurred crashes with some additional info
* 11/09/15: changed the databaseworker in order to save and restore the node_address sets for the crashes with pickle (not compatible with old database files)
* 10/25/15: now the Python SimpleHTTPServer module will be started in the testcase directory if the program option use_http is set
* 10/24/15: implemented the possibility to feed multiple programs with the same input data on one node
