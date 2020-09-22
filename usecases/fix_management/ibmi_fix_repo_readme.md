How to use the ibmi_fix_repo module
========================================

Required dependencies
---------------------

The **ibmi_fix_repo** module manipulates the PTF database via SQLite3.

It requires **SQLite3 >= 3.26**. Install it using `yum install libsqlite3`

## SQLite3 tables

The **ibmi_fix_repo** module stores the PTF repository into following SQLite3 tables:

#### single_ptf_info

|     Column    |                 Type                | Constrain |
|:-------------:|:-----------------------------------:|:---------:|
|       id      |  INTEGER PRIMARY KEY AUTOINCREMENT  |           |
|     ptf_id    |               CHAR(10)              |   UNIQUE  |
|    order_id   |             VARCHAR(50)             |           |
|   file_path   |                 TEXT                |           |
|   file_name   |               CHAR(10)              |           |
|    product    |               CHAR(10)              |   UNIQUE  |
|    release    |               CHAR(10)              |           |
|  description  |                 TEXT                |           |
|    checksum   |                 TEXT                |           |
|   ptf_status  |               CHAR(10)              |           |
| download_time | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |
|    add_time   | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |


#### ptf_group_image_info

|      Column      |                 Type                | Constrain |
|:----------------:|:-----------------------------------:|:---------:|
|        id        |  INTEGER PRIMARY KEY AUTOINCREMENT  |           |
|     order_id     |             VARCHAR(50)             |           |
|     file_path    |                 TEXT                |           |
| ptf_group_number |               CHAR(10)              |   UNIQUE  |
|  ptf_group_level |          INTEGER DEFAULT 0          |   UNIQUE  |
|   release_date   |              TIMESTAMP              |   UNIQUE  |
|      release     |               CHAR(10)              |           |
|    description   |                 TEXT                |           |
|        url       |                 TEXT                |           |
|     ptf_list     |                 TEXT                |           |
|     file_name    |               CHAR(10)              |           |
|     checksum     |                 TEXT                |           |
| ptf_group_status |               CHAR(20)              |           |
|   download_time  | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |
|     add_time     | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |


#### download_status

|        Column       |                 Type                | Constrain |
|:-------------------:|:-----------------------------------:|:---------:|
|          id         |  INTEGER PRIMARY KEY AUTOINCREMENT  |           |
|   download_status   |               CHAR(20)              |           |
|       order_id      |               CHAR(10)              |   UNIQUE  |
|       job_name      |               CHAR(30)              |           |
|      file_path      |                 TEXT                |           |
|     description     |                 TEXT                |           |
|   ptf_group_number  |               CHAR(10)              |           |
|   ptf_group_level   |          INTEGER DEFAULT 0          |           |
|     release_date    |              TIMESTAMP              |           |
| download_start_time | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |
|  download_end_time  | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |
|       add_time      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP |           |


## Checksum

When the **checksum** option is set to `false`, the **ibmi_fix_repo** module processes any database records based on your input parameters.

When the **checksum** option is set to `true`, the **ibmi_fix_repo** module checks the specified physical files and retrieve the checksum data. It also overrides the input parameters if they are not matched when the action is `add` or `update`.

For some special tables or actions, the option **checksum** will be ignored or overridden. For example, deleting records or clearing the table does not require checking any physical file's checksum.

**Possible values of the checksum option**

|        | single_ptf |  ptf_group | download_status |
|:------:|:----------:|:----------:|:---------------:|
|   add  | true/false | true/false |      false      |
| update | true/false | true/false |      false      |
|  find  | true/false | true/false |      false      |
| delete |    false   |    false   |      false      |
|  clear |    false   |    false   |      false      |

## Actions

### add / update

**add**: Insert a new record into the specified table of the PTF repostory's database.
**update**: Update records of the specified table of the PTF repostory's database.

This module processes the action **add** and **update** using an unique SQL syntax **UPSERT**. For more details, please refer to [the SQLite3 manual](https://www.sqlite.org/lang_UPSERT.html "the SQLite3 manual").

#### Required input parameters

|       Type      | Checksum |                     Required parameters                    |
|:---------------:|:--------:|:----------------------------------------------------------:|
|    single_ptf   |   false  |                       ptf_id, product                      |
|    ptf_group    |   false  |       ptf_group_number, ptf_group_level, release_date      |
| download_status |   false  |                          order_id                          |
|    single_ptf   |   true   |                 ptf_id, product, file_path                 |
|    ptf_group    |   true   | ptf_group_number, ptf_group_level, release_date, file_path |
| download_status |   true   |                     order_id, file_path                    |

For type `ptf_group`, some of its input parameters should be retrieved from websites throught the module **ibmi_fix_group_check**.

#### Where the ptf_group data come from

|      Column      |       Data from      |
|:----------------:|:--------------------:|
|     order_id     |      user input      |
|     file_path    |      user input      |
| ptf_group_number | ibmi_fix_group_check |
|  ptf_group_level | ibmi_fix_group_check |
|   release_date   | ibmi_fix_group_check |
|      release     | ibmi_fix_group_check |
|    description   | ibmi_fix_group_check |
|        url       | ibmi_fix_group_check |
|     ptf_list     | ibmi_fix_group_check |
|     file_name    |      file system     |
|     checksum     |      file system     |

**Where the single_ptf data come from**

|   Column  |  Data from  |
|:---------:|:-----------:|
|   ptf_id  |  user input |
|  product  |  user input |
|  release  |  user input |
| file_path |  user input |
| file_name | file system |
|  checksum | file system |

### find

Query records from the specified table of the PTF repostory's database.

The query paramters are used to filter out the matched database records. The **find** action allows you to use any column name as searching criterias. ( When the option **checksum** is `true`, the input parameters should at least contain the **file_path** field.)

**Note**: When the option **checksum** is `true`, the **ibmi_fix_repo** module not only use the input parameters as searching criteria, but also compare the checksum data from speicfied physical files with the input paramters. If the physical files are damaged, the output paramter **db_record** has value `FileNotFound` or `FileNotMatch`.

The matched query result can be found in **success_list** of the output parameters.

### delete

Delete existing records from the specified table of the PTF repostory's database.

The query paramters are used to filter out the database records to delete. If more than one record match, all of them will be deleted.

The **delete** action allows you to use any column name as searching criterias.

### clear

Clear all the records in the specified table. You only need to specify the type of the table. Any other paramters are unnecessary and will be ignored.

## Parameter list

To get better performance, the action add, update and delete execute mulitple SQL statements in batch. That requires the input parameters to follow the same pattern --
```
action: "delete"
type: 'ptf_group'
parameters:
  - {'ptf_group_number':'SF99739', 'ptf_group_level':'30'}
  - {'ptf_group_number':'SF99738', 'ptf_group_level':'10'}
  - {'ptf_group_number':'SF99723', 'ptf_group_level':'20'}
```
But the action **find** is different. It executes mulitple SQL statements one by one. So the input parameters can be flexible --
```
action: "find"
type: 'download_status'
parameters:
  - {'order_id':'2020579181', 'file_path':'/QIBM/UserData/OS/Service/ECS/PTF/2020579181'}
  - {'order_id':'2023203121'}
```

#### Parameter list pattern restrictions

|        | SQL Execution | Parameter Pattern |
|:------:|:-------------:|:-----------------:|
|   add  |     Batch     |       Fixed       |
| update |     Batch     |       Fixed       |
|  find  |   One by One  |      Flexible     |
| delete |     Batch     |       Fixed       |
|  clear |      N/A      |        N/A        |

## Playbook example

This example retrieves data from module **ibmi_fix_group_check** and then insert into the database with module **ibmi_fix_repo**.

For the first time, the example uses the action **add** and set **checksum** to `false` to insert the records without checksum date in case that the PTF group image files are not ready. 

When the image files have been downloaded, it calls action **update** and set **checksum** to `true` to calculate the checksum data and update previous record.

```
---
- hosts: all
  gather_facts: no
  collections:
   - ibm.power_ibmi

  tasks:
    - block:
      - name: query_some_group_info
        ibmi_fix_group_check:
          groups:
            - "SF99738"
        register: group_info

      - name: display_group_info
        debug:
          msg: '{{ group_info.count }} group info returned'

      - name: add_group_info_records
        ibmi_fix_repo:
          database: '/tmp/testdb.sqlite3'
          action: 'add'
          type: 'ptf_group'
          checksum: false
          parameters:
            - {'ptf_group_number':'{{ group_info.group_info[0].ptf_group_number }}', 'ptf_group_level':'{{ group_info.group_info[0].ptf_group_level }}', 'ptf_list':'{{ group_info.group_info[0].ptf_list }}', 'release_date':'{{ group_info.group_info[0].release_date }}'}
        register: add_group_info_records

      - name: display_add_group_info_records
        debug:
          msg: '{{ add_group_info_records }}'

      - name: query_group_info_records
        ibmi_fix_repo:
          database: '/tmp/testdb.sqlite3'
          action: 'find'
          type: 'ptf_group'
          parameters:
            - {'ptf_group_number':'SF99738', 'ptf_group_level':10}
        register: group_info_records

      - name: display_query_group_info_records
        debug:
          msg: '{{ group_info_records.success_list | length }} records returned'

      - name: change_group_info_records
        ibmi_fix_repo:
          database: '/tmp/testdb.sqlite3'
          action: 'update'
          type: 'ptf_group'
          checksum: true
          parameters:
            - {'order_id':'2020579181', 'file_path':'/QIBM/UserData/OS/Service/ECS/PTF/2020579181', 'ptf_group_number':'{{ group_info.group_info[0].ptf_group_number }}', 'ptf_group_level':'{{ group_info.group_info[0].ptf_group_level }}', 'release_date':'{{ group_info.group_info[0].release_date }}'}
        register: change_group_info_records

      - name: display_change_group_info_records
        debug:
          msg: '{{ change_group_info_records }}'

      - name: query_updated_group_info_records
        ibmi_fix_repo:
          database: '/tmp/testdb.sqlite3'
          action: 'find'
          type: 'ptf_group'
          checksum: true
          parameters:
            - {'ptf_group_number':'SF99738', 'ptf_group_level':10}
        register: query_updated_group_info_records

      - name: display_updated_group_info_records
        debug:
          msg: '{{ query_updated_group_info_records }}'

      always:
      - name: drop_the_table
        ibmi_fix_repo:
          database: '/tmp/testdb.sqlite3'
          action: "clear"
          type: 'ptf_group'
```
