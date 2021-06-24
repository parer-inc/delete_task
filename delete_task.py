"""This service allows to delete executed task"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor

r = get_redis()


def delete_task(id):
    """Deletes task from db (table tasks)"""
    cursor, db = get_cursor()
    if not cursor or not db:
        # log that failed getting cursor
        return False
    if id == "ALL":
        q = "DELETE FROM tasks"
    else:
        q = f"DELETE FROM tasks WHERE id={id}"
    try:
        cursor.execute(q)
    except MySQLdb.Error as error:
        print(error)
        # Log
        return False
        # sys.exit("Error:Failed to delete a task")
    db.commit()
    return True


if __name__ == '__main__':

    q = Queue('delete_task', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r,  name='delete_task')
        worker.work()
