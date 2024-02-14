# The xbcrypt command-line options

Usage: 
 
```{.text .no-copy}
$ xbcrypt[OPTIONS]
```

The `xbcrypt` binary has the following command line options:

### decrypt

usage: `-d`  `--decrypt`

Decrypt data input to output.

### encrypt-algo

usage: `-a=name` `--encrypt-algo=name`

Defines the name of the encryption algorithm.

### encrypt-chunk-size

usage: `-s=#` `--encrypt-chunk-size=#`

Defines the size of the working buffer for encryption in bytes. The default value is `64000`.

### encrypt-key

usage: `-k=name` `--encrypt-key=name`

The name of the encryption key.

### encrypt-key-file

usage: `-f=name` `--encrypt-key-file=name`

The name of the file that contains the encryption key.

### encrypt-threads

usage: `--encrypt-threads=#`

This option specifies the number of worker threads used for
parallel encryption/decryption. The default value is 1.

### input

usage: `-i=name` `--input=name`

Defines the name of the optional input file. If the name is not specified, the input reads from the standard input.

### output

usage: `-o=name` `--output=name`

Defines the name of the optional output file. If this name is not specified, the output is written to the standard output.


### read-buffer-size

usage: `--read-buffer-size=#`

Read the buffer size. The default value is 10MB. 

### verbose

usage: `-v` `--verbose`

Display status in verbose mode.
