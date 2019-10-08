# mot-optimizer-table-comparator

Little python script to compare two different PostgreSQL databases

### Usage
```python3 comparator.py <db1> <host1> <port1> <user1> <pass1> <db2> <host2> <port2> <user2> <pass2> --tables <tables_to_check> --name_check --complete --right_to_left --output_path <output_path>```

- ```--tables``` Leave empty for comparing all possible tables. 
- ```--name_check``` Use if you want to check that both databases have the same tables.
- ```--complete```  Use if you want to check names, and right to left tables.
- ```--right_to_left``` Use if you want to see missing rows from left to right, and right to left.
- ```--output``` Directory to save every file. Not using it will save everything in the execution path.


