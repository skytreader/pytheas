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

    import patterns
    import pytheas

    class MyFetcher(patterns.Fetcher):
        # Implementations go

    class MySender(patterns.Sender):
        # Implementations go

    if __name__ == "__main__":
        myfetcher = MyFetcher()
        mysender = MySender()
        daemon = pytheas.Pytheas()
        daemon.run()

Note that there is no need for `nohup` and/or background sigils. A simple
`python` invocation and your code is a [proper Unix daemon](http://legacy.python.org/dev/peps/pep-3143/#correct-daemon-behaviour).

## caveat emptor

Wanted: tests. Never used in production anywhere. Very proof-of-concept.

### will this work in...

**Linux?** Yes.

**Mac?** Should be.

**Windows?** Windows?

## todo

Tests. Use `gevent`. Make stuff configurable. Did I mention tests?

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
