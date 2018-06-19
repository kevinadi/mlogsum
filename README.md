# MongoDB Log Summarizer

This is a small script to quickly summarize events contained in a MongoDB log file, along with some general information about the log file, such as start time, end time, MongoDB version, duration of the log file, etc.

Currently it only supports recent versions of MongoDB.

## Usage

```
mlogsum.py [-h] filename
```

positional arguments:
  `filename`

optional arguments:
  `-h`, `--help`  show this help message and exit
  
## Example

```
$ mlogsum.py mongod.log
{'counters': {'collscan': 58,
              'fatal events': 4,
              'index build': 9,
              'replset reconfig': 1,
              'serverStatus was very slow': 2},
 'filename': 'mongod.log',
 'linecount': 2260,
 'log duration': '4:25:53.903000',
 'log end time': '2018-05-14T13:39:17.146-0500',
 'log start time': '2018-05-14T09:13:23.243-0500',
 'port': '27017',
 'version': 'v3.6.4'}
```
