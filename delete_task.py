"""This service allows to delete executed task"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor


def delete_task(id):
    """Deletes task from db (table tasks)"""
    cursor, db = get_cursor()
    q = f"DELETE FROM tasks WHERE id={id}"
    try:
        cursor.execute(q)
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error:Failed to delete a task")
    cursor.execute()
    db.commit()
    return True


if __name__ == '__main__':
    time.sleep(5)
    r = get_redis()
    q = Queue('delete_task', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r,  name='delete_task')
        worker.work()
