# Raiden

Very simple script to benchmark I/O of RAID devices.

BE CAREFUL running it, it WILL destroy current RAID devices (not all)
and format a new filesystem, destroying all data on the
previous configured RAID device.

Just run **raiden.sh** it and follow the help.

## Analyzing output

The output is human readable and was created for this purpose.
But as stupid human beings that we are it seemed like just
manual inspection would suffice, but in the end we required
some help from machines (when programmed correctly they are
awesome =)).

So we have an analysis tool that you can run with:

```
python analyze.py <file path>
```

This way you can find the best RAID configurations without
manually parsing a long log. The log was not made to be
parsed so the parser is a mess, sorry =(.
