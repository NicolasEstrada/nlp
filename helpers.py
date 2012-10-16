"""Custom functions for document processing """

__author__ = "Mati, Nico"
__version__ = "0.1"


def document_wrapper(input_file):
    """ This function returns a generator for
    each document on the input file.
    """
    counter = 0
    document = []
    for line in input_file:
        if counter == 4:
            yield document
            document = []
            counter = 1
            document.append(line)
        else:
            counter += 1
            document.append(line)

# Example document description (4 lines)
"""
1 Connectivity Versus Entropy
2 Yaser S. Abu-Mostafa
3 1
4
"""


def insert_into_mysql(table, cols, rows):
    """This function insert into mysql the required rows."""

    import MySQLdb as mdb

    con = None

    try:

        con = mdb.connect('localhost', 'mestrada',
            '123456', 'inf335')
        # Check if the connection has been stablished
        if con:
            cur = con.cursor()

            query = "INSERT INTO " + table + " ( " + ', '.join(cols) + ") VALUES ("
            query += ", ".join(["%s" for i in range(0, len(cols))])
            query += ")"

            if len(rows) > 1:
                cur.executemany(query, rows)
            elif len(rows) == 1:
                cur.execute(query, rows[0])

            # print cur._last_executed

            con.commit()
        else:
            print "Connection problem"

    except mdb.Error, e:
        print "[MySql] Error ", e

    finally:
        if con:
            con.close()
