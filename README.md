# Push notifications on your Android phone for HTCondor jobs on completion

It's a single Python script, which parses the `condor_q USERNAME` output and sends a push notification to your phone using the [Pushover](https://www.pushover.net) service. Try `./condor_notify.py --help` for more information.

**Usage:**

```
CONDOR_USERNAME=foo
PUSHOVER_USER=abc123xyz
PUSHOVER_TOKEN=ijk456def
python condor_notify.py $CONDOR_USERNAME $PUSHOVER_USER $PUSHOVER_TOKEN
```
