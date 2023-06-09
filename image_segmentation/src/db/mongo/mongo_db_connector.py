import logging
import os

from gridfs import GridFS
from pymongo import MongoClient


class MongoDBConnector:
    """The MongoDBConnector class provides a connection to a MongoDB database
        and allows the user to download or upload files to the GridFS file system in the database.
        The connection parameters are read from environment variables.

    Methods:

    enter: establishes a connection to the database and returns the instance of the class
    exit: closes the connection to the database
    download_file: downloads a file from the GridFS file system by the given filename
    upload_file: uploads a file to the GridFS file system with the given filename and bytes
    Raises:

    Exception: when the MongoDBConnector is not initialized.
    """

    def __init__(self):
        self.host = os.environ.get("MONGO_HOST")
        self.port = os.environ.get("MONGO_PORT")
        self.db_name = os.environ.get("MONGO_DBNAME")
        self.username = os.environ.get("MONGO_USERNAME")
        self.password = os.environ.get("MONGO_PASSWORDD")
        self.conn = None
        self.db = None
        self.fs = None

    def __enter__(self):
        uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        logging.info(uri)
        self.conn = MongoClient(uri)

        self.db = self.conn.grid_file
        self.fs = GridFS(self.db)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.db = None
            self.fs = None

    def download_file(self, filename):
        if self.fs is None:
            raise Exception("MongoDBConnector not initialized.")
        file = self.db.fs.files.find_one({"filename": filename})
        return file

    def upload_file(self, filename: str, file: bytes) -> None:
        if self.fs is None:
            raise Exception("MongoDBConnector not initialized.")
        self.fs.delete(filename=filename)
        new_file = self.fs.new_file(filename=filename)

        new_file.write(file)

        new_file.close()
