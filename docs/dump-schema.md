# Dump schema for all tables

This script is designed to dump the schemas of all tables from each database in a MySQL server instance, excluding the system databases, into separate files.

The script should be modified for your specific use case before you run it. For example, you may want to exclude certain tables or databases, or specify a different output directory.

```shell
print_usage() {
    echo "Usage: $0 [--defaults-file=<file>] [--destination-dir=<directory>]"
    echo "  --defaults-file=<file>      (Optional) Path to MySQL defaults file (e.g., /etc/my.cnf)"
    echo "  --destination-dir=<directory> (Optional) Directory to save the schema dumps (default: schema_dumps)"
    exit 1
}

USER=""
DEFAULTS_FILE=""
HARDCODED_PASSWORD="test2"
DEST_DIR="schema_dumps"

# Check for -h or --help option
if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    print_usage
fi

# Parse arguments using a loop to check for --defaults-file and --destination-dir options
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --defaults-file=*)
            DEFAULTS_FILE="--defaults-file=${1#*=}"
            echo "Using provided defaults file: ${1#*=}"
            ;;
        --destination-dir=*)
            DEST_DIR="${1#*=}"
            echo "Saving schema dumps in: $DEST_DIR"
            ;;
        *)
            echo "Error: Invalid option '$1'"
            print_usage
            ;;
    esac
    shift
done

# Default behavior if no defaults-file is provided
if [ -z "$DEFAULTS_FILE" ]; then
    if [ -n "$MYSQL_PWD" ]; then
        echo "Using password from environment variable MYSQL_PWD"
    else
        DEFAULTS_FILE="--password=$HARDCODED_PASSWORD"
        echo "Using hardcoded password in the script"
    fi
    USER="-uroot"
    echo "Using hardcoded user: $USER"
fi

mkdir -p "$DEST_DIR"  # Root directory for schema dumps
echo "Schema will be saved in: $DEST_DIR"

# Get the list of all databases, excluding system databases
databases=$(mysql $DEFAULTS_FILE $USER -N -e "SHOW DATABASES" | grep -Ev "^(information_schema|performance_schema|mysql|sys)$")

for db in $databases; do
    echo "Dumping schemas for database: $db"

    mkdir -p "$DEST_DIR/$db"  # Create a directory for each database

    # Dump only the database creation statement
    mysqldump $DEFAULTS_FILE $USER --no-data --databases "$db" > "$DEST_DIR/$db/create_database_${db}.sql"

    # Get the list of tables for the current database
    tables=$(mysql $DEFAULTS_FILE $USER -N -e "SHOW TABLES FROM $db")

    for table in $tables; do
        echo "  Dumping schema for table: $table"

        # Ensure `USE <database>;` is at the top of each table's schema file
        echo "USE \`$db\`;" > "$DEST_DIR/$db/${table}.sql"

        # Append the table schema dump
        mysqldump $DEFAULTS_FILE $USER --no-data --skip-add-drop-table "$db" "$table" >> "$DEST_DIR/$db/${table}.sql"
    done
done

echo "Schema dumps are saved in the '$DEST_DIR' directory."

```

## Usage

To use this script, follow these steps. Run all the commands as root or use the sudo command.

1. Save the script  

    * Copy the script to your local machine.  

    * Save the file with a `.sh` extension, such as `dump_schemas.sh`.  

2. Make the script executable  

    * Run the following command to make the script executable:  

      ```shell
      chmod +x dump_schemas.sh
      ```  

3. Verify dependencies  

    * Check if `mysqldump` is installed by running:  

      ```shell
      which mysqldump
      ```  

    * If `mysqldump` is not installed or not available in your PATH, install it using:  

      ```shell
      sudo apt install mysql-client
      ```  

4. Use one of the following commands to execute the script:
   
    * See the usage instructions, run:
   
        ```shell
        ./dump_schemas.sh --help
        ```  
   
    * Specify a MySQL defaults file (for example, `~/.my.cnf`) and destination directory for the schema dumps, run:
   
        ```shell
        ./dump_schemas.sh --defaults-file=/path/to/my.cnf --destination-dir=/path/to/output
        ```  
   
    * If you do not have a `defaults-file`, use the script defaults of a hardcoded password or an environment variable, if set. Specify only the destination directory:
    
        ```shell
        ./dump_schemas.sh --destination-dir=/path/to/output
        ```  
      
      * To use the hardcoded password and default destination directory, `schema_dumps`, use:
    
        ```shell
        ./dump_schemas.sh 
        ```  
    


5. Inspect the output  

    * The script creates a `schema_dumps` directory in the current working directory.  

    * The dumped schemas are organized as follows:  

        ```shell
        find .
        ```
            
        ??? example "Expected output"
        
            ```{.text .no-copy}
            .
            ./test
            ./test/t4.sql
            ./test/t3.sql
            ./test/create_database_test.sql
            ./test2
            ./test2/create_database_test2.sql
            ./test2/create_database_test2.sql
            ./test2/t1.sql
            ...
            ```  

6. Review logs for errors or warnings  

    * After execution, check the terminal output for any errors or warnings that may indicate issues with the backup process.  
    

## Troubleshooting

If you encounter any issues while using this script, please check the following:

* Ensure that `mysqldump` is installed and available in your PATH.

* Verify that the MySQL root user and password are correct.

* Check the permissions of the output directory and ensure that the script has write access.

* Ensure that the MySQL server is running and accessible.

* Ensure that the MySQL server is configured to accept remote connections.
