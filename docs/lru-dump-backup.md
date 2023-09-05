
# LRU dump backup

*Percona XtraBackup* includes a saved buffer pool dump into a backup to enable
reducing the warm up time. It restores the buffer pool state from
`ib_buffer_pool` file after restart. *Percona XtraBackup* discovers
`ib_buffer_pool` and backs it up automatically.


![image](_static/lru_dump.png)

If the buffer restore option is enabled in `my.cnf`, buffer pool will be in
the warm state after backup is restored.

Find the information on how to save and restore the buffer pool dump in [Saving and Restoring the Buffer Pool State](https://dev.mysql.com/doc/refman/8.1/en/innodb-preload-buffer-pool.html).