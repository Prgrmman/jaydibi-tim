# Flask playground

I created this little sandbox to experiment with flask development.
Everything has been configured using pipenv with python 3.7.

As a bit of fun, it's actually possible to run this entire suite from an android phone directly using the termux app (on the google play store).

Simply clone the repository, navigate to this directory, and run

```
pipenv install
```

When doing this at the time (May 2020), I found that the python package maintained by the termux environment was only at 3.6.
To get around this problem, you can edit the lock file, but don't commit it.
