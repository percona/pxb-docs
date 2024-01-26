# The xbstream command-line options

This utility has a tar-like interface.


The xbstream binary has the following options:

## c

Usage: `-c`

Streams files specified on the command line to its standard output.

## decrypt

Usage: `--decrypt=ALGO`

Specifies that xbstream automatically decrypts encrypted files when extracting input stream. The supported values are: `AES128`, `AES192`, and `AES256`. 

You can specify either `--encrypt-key` or `--encrypt-key-file` to provide the encryption key, but do not use both options. 

## encrypt-key 

Usage: `--encrypt-key`

Specify the encryption key used. Do not use this option with `--encrypt-key-file`; the options are mutually exclusive.

## encrypt-key-file

Usage: `--encrypt-key-file`


Specify the file that contains the encryption key. Do not use this option with `--encrypt-key`; the options are mutually exclusive.

## encrypt-threads

Usage: `--encrypt-threads`

Specify the number of threads for parallel data encryption. The default value is `1`. 

## x

Usage: `-x`

Extracts files from the stream read from its
standard input to the current directory unless specified otherwise with the
`-c` option. Support for parallel extraction with the `--parallel`
option
