
# Encrypted backup with the component_keyring_file`

The server uses a manifest to load the component during startup and the component uses a configuration file for the necessary settings. The component is stored in the directory named by the `plugin_dir` variable.

See the [MySQL documentation on the component 
installation](https://dev.mysql.com/doc/refman/8.0/en/keyring-component-installation.html) for more 
information. 

With the appropriate privilege and the file-based keyring component active, you can `SELECT` on
the [performance_schema.keyring_component_status table](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-keyring-component-status-table.html)
to view the attributes and status of the installed keyring component.

## Examples

This manifest loads a file-based keyring component:

```json
{
   "components": "file://component_keyring_file"
}
```

The loaded keyring component uses this configuration file:

```json
{
   "path": "/var/lib/mysql-keyring/keyring_file", "read_only": false
}
```