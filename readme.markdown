# pytheas

A very small framework for a very simple pattern: most networking daemon apps
_fetch_ data from some source, parse that data, and, based on data contents,
_send_ it elsewhere.

## why?

Just because I'm so tired seeing daemon logic, fetching logic, and sending logic
all in one place.

## what for?

You probably won't want to use this for low-level networking. I intend this to
be used in the [OSI Application Layer](http://en.wikipedia.org/wiki/Application_layer).

## how?

As simple as...

    import pytheas.patterns
    import pytheas.sfdaemon

    class MyFetcher(pytheas.patterns.Fetcher):
        # Implementations go

    class MySender(pytheas.patterns.Sender):
        # Implementations go

    if __name__ == "__main__":
        myfetcher = MyFetcher()
        mysender = MySender()
        daemon = pytheas.sfdaemon.Pytheas()
        daemon.run()

Then, invoke your code as follows to [properly daemonize](http://legacy.python.org/dev/peps/pep-3143/#correct-daemon-behaviour):
    
    nohup python codesrc.py > codesrc.out 2> &1 &

See [this](http://stackoverflow.com/a/2423550/777225) StackOverflow answer for
more details on the invocations.

See the examples for concrete examples.

### wait a minute...

Yah. The early stages of this project wanted to feature the capability of creating
daemons without having to use `nohup` and all those sigils. It used
[python-daemon](https://pypi.python.org/pypi/python-daemon/1.5.5) to achieve that
effect. However, as of this writing, it has been more than four years since
python-daemon was last updated and,
[as I found out](https://github.com/skytreader/pytheas/commit/26b26fa1bc56bd66c7b8fc01715bf84d1e3ffb5f),
python-daemon is not compatible with gevent.

### so that's it?

[geventdaemon](https://github.com/gwik/geventdaemon) looks worth a try but
(again as of this writing) it has been two years since the last commit so I'm
not expecting much.

If you want to give it a try (or maybe hack your own compatibility layer), just
give me a shout (or a pull request).

## other features

### commands server

You can communicate with a running daemon via the command server. By default,
Pytheas listens to port 16981. You can specify your own port via the constructor
of Pytheas.

    pytheas.sfdaemon.Pytheas(fetcher, sender, port=8888)

You can also create your own command handler and pass it to the Pytheas
constructor as follows:

_TODO_: Expand on this

    pytheas.sfdaemon.Pytheas(fetcher, sender, command_interpreter=my_interpreter)

Q: I'm stingy with ports and don't need to signal to my daemons anyway. Can I
instruct Pytheas to _not run_ the command server?  
A: Yes. Just pass `port=None` to the Pytheas constructor.

Q: What's the format for commands?  
A: You can specify your own format for your own interpreter as long as it takes
the newline character (`\n`) as a terminator. However, the reserved commands of
Pytheas use JSON so you may want to adopt that for the sake of world peace.

Q: What are Pytheas' reserved commands?  
A: Coming soon...

## caveat emptor

Wanted: more tests. Never used in production anywhere. Very proof-of-concept.

See also, **todo** below.

### will this work in...

**Linux?** Yes.

**Mac?** Should be.

**Windows?** Windows?

## todo

More tests. Make stuff configurable. Did I mention more tests? What about better
tests?

Also...

  - Ensure fail-fast behavior.
  - Allow for different fetch-send patterns (basic, queued, etc.).

# Running examples

The examples fetch and send via Redis queues. The import path assume that Pytheas
is installed in your system. This package is now in PyPI so just do

    pip install Pytheas

# License

The MIT License (MIT)

Copyright (c) 2014 Christian Andrei Estioco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
