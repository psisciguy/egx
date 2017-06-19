#
# state_tracker.py
#
# Common startup file for eGX MVP0
# - MVP0 = basic level getting started code-base
#
# Functions
# - connect to database (sqlite)
# - create data stores (if not present)
# - load initial data (if not loaded yet)
# - update tables: entire rows, or partial rows
#
# Works With
# - eGX_state.db
# - discover_units.py
# - basic_stim_cmd.py
# - system_test.py

import sqlite3
from sqlite3 import Error

db_file = "state_db.sqlite"

# BACKUP table creation commands... May need later-on
sql_create_system_table = """ 
    CREATE  TABLE "main"."system" ("index" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , 
    "install_datetime" DATETIME, "num_EC" INTEGER DEFAULT 0, "num_MC" INTEGER DEFAULT 0, 
    "powerdown_count" INTEGER, "customer_code" VARCHAR, "site_code" VARCHAR, "site_name" TEXT, 
    "stim_unit_nolite_cal_value" INTEGER DEFAULT 0, "mc_cal_current_100uT" INTEGER DEFAULT 0, 
    "ch1_discovered" BOOL NOT NULL  DEFAULT 0, "ch2_discovered" BOOL NOT NULL  DEFAULT 0, 
    "ch3_discovered" BOOL NOT NULL  DEFAULT 0, "ch4_discovered" BOOL NOT NULL  DEFAULT 0);
    """

sql_create_stimunit_table = """
    CREATE TABLE "stim_units" ("index" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "channel" INTEGER NOT NULL , 
    "discovered_address" CHAR NOT NULL , "discovered_datetime" DATETIME NOT NULL , "serial_number" INTEGER, 
    "fw_version" VARCHAR, "hw_version" VARCHAR, "device_type" VARCHAR, "model_number" INTEGER, 
    "powerdown_count" INTEGER, "op_hours" FLOAT, "electrode_type" VARCHAR, "grow_medium" VARCHAR, 
    "init_protocol" INTEGER, "day_protocol" INTEGER,  "night_protocol" INTEGER, "last_protocol_step" INTEGER, 
    "last_cmd_rx_datetime" DATETIME, "light_trigger_mode" INTEGER, "last_medium_resistance" INTEGER, 
    "average_medium_resistance" INTEGER)
    """

sql_create_protocol_table = """
    CREATE  TABLE "main"."stim_protocols" ("index" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , 
    "name" VARCHAR NOT NULL , "description" TEXT, "multi_step_enabled" BOOL NOT NULL  DEFAULT 0, "voltage" INTEGER, 
    "freq" INTEGER, "dutycycle" INTEGER, "on_time_sec" INTEGER, "off_time_sec" INTEGER, "max_current_mA" INTEGER, 
    "next_step" INTEGER, "step_delay_seconds" DOUBLE, "max_loop_count" DOUBLE, "protocol_code" char(15))
    """

######################
######################

def main():

    # create a database connection
    conn = create_connection(db_file)
    if conn is not None:
		with conn:
			print("Query all stim_units")
        	select_all_stim_units(conn)
			
    else:
        print("Error! cannot create the database connection.")


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_all_stim_units(conn):
    """
    Query all rows in the stim_units table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM stim_units")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)



# def create_table(conn, create_table_sql)
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)

if __name__ == '__main__':
    main()