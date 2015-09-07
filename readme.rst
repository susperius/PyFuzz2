PyFuzz2
=======

This toolset is a fuzzing framework, you can use it to fuzz-test software on multiple machines.
It consists of a client and a server component. The clients are able to run in network and single mode.
The main difference is in network mode you can use the servers web frontend to change the config of your
clients and all crashes are send to the server and collected by image name (but there is much to do in order to
make the whole web frontend more functional).
I used these tools to fuzz browsers and I got multiple crashes on the major ones (chrome, iexplore, firefox), but
nothing security relevant.
My fuzzer for browsers is included in the client part. The reducer for javascript parts is also included.
A css and html reducer is on the todo list.
There is also a real dump bytemutation fuzzer included.
You can easily add your own fuzzer, all you have to do is inherit from *fuzzing.fuzzer* and implement all the
necessary methods. After this you add your fuzzer to the dictionary in *fuzzing.fuzzers*. Now you can use your
own fuzzer.

For the client/server you need the following modules and software installed:

* WinDbg
* PyKd
* Gevent

Both software parts are configured via xml files. The config-files show some possible values and example of how to
config the client/server.

You should **never** use this software in open networks (e.g. internet) there are no checks implemented to
identify corrupted data and no login is required to access the web-frontend!

