# Push notifications on your Android phone for HTCondor jobs on completion

It's a single Python script, which parses the `condor_q USERNAME` output and sends a push notification to your phone using the [Pushover](www.pushover.net) service.

**Usage:**

```
python condor_notify.py john_doe xyzabc123 klm987ijk
```
