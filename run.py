import os, time, sys, json
from database.connection import Connection

dbOption = None ## redshift cluster connection
isVerbose = 0
qryDir = "sql-qry/batch-1-folder/" ## default directory for queries
countRunWithoutResult, countRunWithResult, countError = 0, 0, 0
withResultList, withoutResultList, withErrorList = [], [], []

## test redshift connection
def test(db_ops, dbschema):

    res = db_ops.query(dbschema, "SELECT * FROM %s.concept limit 5;" % dbschema)
    if res:
        print "[INFO] redshift connection test - passed!"
    else:
        print "[DEBUG] redshift connection test - faild, please check connection details!"


def executeAllQueries(db_ops, dbschema, queryDir, verbose):

    print "[INFO] is verbose: %s" % (verbose)

    directory = os.path.normpath(queryDir)
    global countRunWithoutResult, countRunWithResult
    global withResultList, withoutResultList

    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".sql"):
                f=open(os.path.join(subdir, filename),'r')
                qry = f.read()
                print "============================================================"
                print "[INFO] EXECUTE QUERY: (%s)" % filename

                if verbose == 1:
                    print "[INFO] query execute: [%s]" % (qry)
                
                start_time = time.time()
                result = db_ops.query(dbschema, qry)

                if verbose == 1:
                    if len(result) < 500:
                        print "[INFO] query results: "
                        print result
                    else:
                        print result[:500]

                end_time = time.time()
                    
                if result != None:
                    countRunWithResult += 1
                    withResultList.append(filename)
                    print "[INFO] query successfully ran, result (%s) rows, time (%s)." % (str(len(result)), (end_time - start_time))
                else:
                    countRunWithoutResult += 1
                    withoutResultList.append(filename)
                    print "[INFO] query successfully ran without any result, time (%s)." % (str(len(result)), (end_time - start_time))

                f.close()


def main():
    global isVerbose, qryDir

    if len(sys.argv) > 3:
        dbOption = str(sys.argv[1])
        qryDir = str(sys.argv[2])
        isVerbose = str(sys.argv[3])
        print "[INFO] Ready to execute queries in directory: " + qryDir
    else:
        print "Usage: python run.py <redshift db, options in config/config.json> <directory for queries> <isVerbose OPTIONS (0: not verbose, 1: verbose)>"
        sys.exit(1)

    with open('config/config.json') as config_file:
        conf = json.load(config_file)
        if not dbOption or dbOption not in conf:
            print "[ERROR] database option not found, please check if it's configured in config/config.json!"
            sys.exit(1)

        DB_NAME = conf[dbOption]["dbname"]
        HOST = conf[dbOption]["host"]
        PORT = conf[dbOption]["port"]
        USERNAME = conf[dbOption]["user"]
        PASSWORD = conf[dbOption]["passwd"]
        DB_SCHEMA = conf[dbOption]["dbschema"]

        print "[INFO] redshift cluster: %s.%s" % (DB_NAME, DB_SCHEMA)
        db_ops = Connection(DB_NAME, HOST, PORT, USERNAME, PASSWORD)

        test(db_ops, DB_SCHEMA)
        executeAllQueries(db_ops, DB_SCHEMA, qryDir, isVerbose)


if __name__ == "__main__":

    main()

    print "=========================== SUMMARY ============================"
    print "Number of queries that successfully executed with results: (%s)" % (countRunWithResult)
    print "List of queries run with results:"
    if withResultList:
        print withResultList
    print "----------------------------------------------------------------"

    print "Number of queries that successfully executed without results: (%s)" % (countRunWithoutResult)
    print "List of queries run without results:"
    if withoutResultList:
        print withoutResultList
    print "----------------------------------------------------------------"
    print "Number of queries that run with error (%s)" % (countError)
    print "List of query with error: "
    if withErrorList:
        print withErrorList
    
