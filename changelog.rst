* 01/11/15: redesigned the debugger to really avoid race conditions, in order to do this the childdbg windbg option is used
* 01/05/15: redesigned the reducingworker in order to use the new debugging approach and to traverse through the result directories instead of the testcase directory; added a 2 seconds delay in template.dat in order to avoid/minimize race conditions, while the debugger is looking for the processes and attaching to them
* 12/22/15: if you delete a node in the web interface, it'll be also deleted from the database; you can now configure in which interval the server is requesting the node configs; the size of the canvas part is now configurable; node reboot time is now adjustable
* 11/16/15: implemented a canvas fuzzer for 2D canvas elements
* 11/11/15: implemented the stats page in the web interface; this site lists the occurred crashes with some additional info
* 11/09/15: changed the databaseworker in order to save and restore the node_address sets for the crashes with pickle (not compatible with old database files)
* 10/25/15: now the Python SimpleHTTPServer module will be started in the testcase directory if the program option use_http is set
* 10/24/15: implemented the possibility to feed multiple programs with the same input data on one node
