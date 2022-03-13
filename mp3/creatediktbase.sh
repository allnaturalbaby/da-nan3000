#!/bin/bash

 $(sqlite3 diktbase.db < diktbase.sql)
 $(sqlite3 diktbase.db < eksempeldata.sql)