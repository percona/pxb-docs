# Using environment variable files (.env) with xbcloud

Environment variable files (`.env`) are a common way to manage configuration settings and sensitive credentials. Here's how to use them with xbcloud:

## Creating a .env file

Create a `.env` file in your project directory or a secure location:

### S3 example
```{.bash data-prompt="$"}
# Example .env file for S3
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-west-2
AWS_ENDPOINT=https://s3.us-west-2.amazonaws.com
```

### Swift example
```{.bash data-prompt="$"}
# Example .env file for Swift
OS_AUTH_URL=http://192.168.1.100:5000/v3
OS_USERNAME=admin
OS_PASSWORD=secret
OS_PROJECT_DOMAIN=default
OS_USER_DOMAIN=default
```

### Azure example
```{.bash data-prompt="$"}
# Example .env file for Azure
AZURE_STORAGE_ACCOUNT=mystorageaccount
AZURE_CONTAINER_NAME=backups
AZURE_ACCESS_KEY=your-access-key-here
```

## Loading environment variables

Environment variables from `.env` files are not automatically loaded by the shell. You need to explicitly load them before running xbcloud. Here are three methods to accomplish this:

### Method 1: using `source` or `.` command

The `source` command (or its shorthand `.`) reads and executes commands from a file in the current shell environment. This makes all variables from the `.env` file available to subsequent commands in the same shell session.

```{.bash data-prompt="$"}
# Load the environment variables
source .env
# or
. .env

# Now run xbcloud
xtrabackup --backup --stream=xbstream | xbcloud put s3://my-bucket/backup-$(date +%Y%m%d)
```

### Method 2: using `env` command

The `env` command runs another program with a modified environment. Combined with `cat .env | xargs`, it reads the `.env` file and passes the variables as arguments to `env`, which then sets them for the command that follows.

You can run xbcloud with variables loaded from a .env file in a single command:

```{.bash data-prompt="$"}
# Run xbcloud with environment variables from file
env $(cat .env | xargs) xtrabackup --backup --stream=xbstream | xbcloud put s3://my-bucket/backup-$(date +%Y%m%d)
```

This approach is convenient but fragile:

* This method can break if values contain spaces, quotes, or special shell characters (!, &, $, etc.).

* Quoting inside .env files doesn't always survive the `xargs` parsing.

For sensitive credentials or values with special characters, Method 1 or Method 3 is safer.

### Method 3: using `export` with a script

This method creates a shell script that loads environment variables and runs the backup command. The `set -a` command automatically exports all variables that are set, making them available to child processes. This is useful for automation because it bundles variable loading and the backup command together.

Create a script that loads the environment variables:

```{.bash data-prompt="$"}
#!/bin/bash
# load-env.sh

set -a  # automatically export all variables
source .env
set +a  # stop automatically exporting

# Run your backup command
xtrabackup --backup --stream=xbstream | \
  xbcloud put s3://my-bucket/backup-$(date +%Y%m%d)
```

Make it executable and run:
```{.bash data-prompt="$"}
chmod +x load-env.sh
./load-env.sh
```

## Security best practices

* File permissions: Set restrictive permissions on your `.env` file:
  ```{.bash data-prompt="$"}
  $ chmod 600 .env  # Only owner can read/write
  ```

* Gitignore: Add `.env` to your `.gitignore` file to prevent committing sensitive data:
  ```{.bash data-prompt="$"}
  echo ".env" >> .gitignore
  ```

* Template file: Create a `.env.example` file with placeholder values:
  ```{.bash data-prompt="$"}
  # .env.example
  AWS_ACCESS_KEY_ID=your-access-key-here
  AWS_SECRET_ACCESS_KEY=your-secret-key-here
  AWS_DEFAULT_REGION=us-west-2
  ```

* Location: Store `.env` files in a secure location, not in your project root if possible:
  ```{.bash data-prompt="$"}
  # Store in a secure directory
  /etc/xtrabackup/.env
  /home/backup/.env
  ```

## Complete example

Here's a complete example of using a `.env` file with xbcloud. This example demonstrates the full workflow from creating the environment file to running a backup:

```{.bash data-prompt="$"}
# 1. Create the .env file
cat > /secure/path/.env << EOF
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=us-west-2
AWS_ENDPOINT=https://s3.us-west-2.amazonaws.com
EOF

# 2. Set secure permissions
chmod 600 /secure/path/.env

# 3. Load environment variables and run backup
source /secure/path/.env
xtrabackup --backup --stream=xbstream --target-dir=/tmp/backup | \
xbcloud put s3://my-backup-bucket/backup-$(date +%Y%m%d-%H%M%S)
```

This example shows the complete process:

* Step 1: The `cat > /secure/path/.env << EOF` command creates a new `.env` file using a here document. The `<< EOF` syntax allows you to write multiple lines until it encounters the `EOF` marker, making it easy to create files with multiple environment variables.

* Step 2: The `chmod 600` command sets file permissions so that only the owner can read and write the file (no access for group or others), which is essential for protecting sensitive credentials.

* Step 3: The `source` command loads the environment variables from the `.env` file into the current shell session, then the backup pipeline runs:

  * `xtrabackup --backup --stream=xbstream --target-dir=/tmp/backup` creates a backup and streams it in xbstream format

  * The pipe (`|`) passes the streamed backup data to the next command

  * `xbcloud put s3://my-backup-bucket/backup-$(date +%Y%m%d-%H%M%S)` uploads the backup to the S3 bucket with a timestamped name

## Troubleshooting .env files

* Check if variables are loaded:
  ```{.bash data-prompt="$"}
  source .env
  echo $AWS_ACCESS_KEY_ID  # Should show your access key
  ```

* Verify file format: Ensure no spaces around the `=` sign:
  ```{.bash data-prompt="$"}
  # Correct
  AWS_ACCESS_KEY_ID=value
  
  # Incorrect (will not work)
  AWS_ACCESS_KEY_ID = value
  ```

* Handle special characters: Quote values with special characters:
  ```{.bash data-prompt="$"}
  OS_PASSWORD="my-password-with-special-chars!"
  ```

* Comments: Use `#` for comments in `.env` files:
  ```{.bash data-prompt="$"}
  # This is a comment
  AWS_ACCESS_KEY_ID=your-key-here
  ```

## Integration with scripts and automation

For automated backups, you can create a wrapper script:

```{.bash data-prompt="$"}
#!/bin/bash
# backup-script.sh

# Load environment variables
if [ -f "/secure/path/.env" ]; then
    source /secure/path/.env
else
    echo "Error: .env file not found"
    exit 1
fi

# Run backup
xtrabackup --backup --stream=xbstream --target-dir=/tmp/backup | \
xbcloud put s3://my-backup-bucket/backup-$(date +%Y%m%d-%H%M%S)

echo "Backup completed successfully"
```

This approach provides a secure, maintainable way to manage xbcloud credentials and configuration without exposing sensitive information in command lines or scripts.
