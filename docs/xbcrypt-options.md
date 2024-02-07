# The xbcrypt command-line options

The `xbcrypt` binary has the following command line options:

### encrypt-algo

usage: `-a` `--encrypt-algo`

Defines the name of the encryption algorithm.

### decrypt

usage: `-d`  `--decrypt`

Decrypt data input to output.

### encrypt-chunk-size

usage: `-s` `--encrypt-chunk-size`

Defines the size of the working buffer for encryption in bytes. The default value is `64000`.

### encrypt-key

usage: `-k` `--encrypt-key`

The name of the encryption key.

### encrypt-key-file

usage: `-f` `--encrypt-key-file`

The name of the file that contains the encryption key.

### encrypt-threads

usage: `--encrypt-threads`

This option specifies the number of worker threads used for
parallel encryption/decryption.

### input

usage: `-i` `--input`

Defines the name of the optional input file. If the name is not specified, the input reads from the standard input.

### output

usage: `-o` `--output`

Defines the name of the optional output file. If this name is not specified, the output is written to the standard output.

### verbose

usage: `-v` `--verbose`

Display status in verbose mode.
