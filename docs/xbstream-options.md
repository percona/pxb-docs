# The xbstream command-line options

```{.text .no-copy}
$ xbstream -c [OPTIONS]
$ xbstream -x [OPTIONS]
```

This utility has a tar-like interface.


The xbstream binary has the following options:

## absolute-names

Usage: `-absolute-names`

Do not strip the leading // (slashes) from the file names when creating archives.

## c

Usage: `-c`

Streams files specified on the command line to its standard output.

## decompress

Usage: `--decompress`

Decompress the individual backup files

## decompress-threads

Usage: `--decompress-threads=#`

The number of threads for parallel data decompression. The default value is 1.

## decrypt

Usage: `--decrypt=name`

Specifies that xbstream automatically decrypts encrypted files when extracting input stream. The supported values are: `AES128`, `AES192`, and `AES256`. 

You can specify either `--encrypt-key` or `--encrypt-key-file` to provide the encryption key, but do not use both options. 

## directory

Usage: `--directory=name`

Change the current directory to this named directory before streaming or extracting.

## encrypt-key 

Usage: `--encrypt-key=name`

Specify the encryption key used. Do not use this option with `--encrypt-key-file`; these options are mutually exclusive.

## encrypt-key-file

Usage: `--encrypt-key-file=name`

Specify the file that contains the encryption key. Do not use this option with `--encrypt-key`; these options are mutually exclusive.

## encrypt-threads

Usage: `--encrypt-threads-=#`

Specify the number of threads for parallel data encryption. The default value is `1`. 

## extract

Usage: `--extract`

Extract to disk the files from the stream to the standard input.

## fifo-dir

Usage: `--fifo-dir=name`

The directory used to read or write named pipes.

## fifo-streams

Usage: `--fifo-streams=#`

The number of FIFO files (named pipes) to use for parallel data file streaming. To disable the option and send the stream to STDOUT, set the value to 1. 

## fifo-timeout

Usage: `--fifo-timeout=#`

The number of seconds to wait for the other end to open the stream. The default value is 60.

## parallel

Usage: `--parallel=#`

Defines the number of worker threads for reading or writing.


## x

Usage: `-x`

Extracts files from the stream read from its
standard input to the current directory unless specified otherwise with the
`-c` option. Support for parallel extraction with the `--parallel`
option

## verbose

Usage: `--verbose`

Print verbose output
