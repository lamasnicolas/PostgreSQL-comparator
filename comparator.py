import argparse

from db_checker import DbCompare, Parameters

parser = argparse.ArgumentParser(description='The program will check if two PostgreSQL databases contains the same '
                                             'tables and same rows in each one. '
                                             'Default behaviour is to check contents for each table in db 1.')

parser.add_argument("db1", help="Name of the first database")
parser.add_argument("host1", help="Host location of the first database")
parser.add_argument("port1", help="Port of the first database")
parser.add_argument("user1", help="Username for the first database")
parser.add_argument("pass1", help="Password for the first database")

parser.add_argument("db2", help="Name of the second database")
parser.add_argument("host2", help="Host location of the second database")
parser.add_argument("port2", help="Port of the second database")
parser.add_argument("user2", help="Username for the second database")
parser.add_argument("pass2", help="Password for the second database")

parser.add_argument("-t", "--tables", help="Tables to be checked. Leaving this empty will check all tables.", nargs="*",
                    type=str, default=[])
parser.add_argument("-n", "--name_check", action="store_true", help="Will check that both databases contains the same "
                                                                    "tables, and then will check contents.")
parser.add_argument("-c", "--complete", action="store_true", help="Will do every check available.")
parser.add_argument("-rl", "--right_to_left", action="store_true", help="Will do the check queries for each table for"
                                                                        "both sides (Default is row contained in table "
                                                                        "from db one, check if it exists in same table "
                                                                        "in db two)")
parser.add_argument("-o", "--output_path", type=str, default="", help="Location of the output folder. Do not use / at the end"
                                                                      " (Default is the same location that the script is run)")

args = parser.parse_args()

params = Parameters(args.db1, args.host1, args.port1, args.user1, args.pass1,
                    args.db2, args.host2, args.port2, args.user2, args.pass2,
                    args.tables, args.name_check, args.complete, args.right_to_left,
                    args.output_path)

dc = DbCompare(params)
dc.process()
