import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from google.cloud import secretmanager

class SecMan:
    def __init__(self):
        project_id = ""
        secret_id = ""
        version_id = ""
        self.client = secretmanager.SecretManagerServiceClient()
        self.name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        self.secret = self.client.access_secret_version(request={"name": self.name}).payload.data.decode("UTF-8")
        self.env = None
        if self.secret:
            self.secret = [x.strip() for x in self.secret.split("\n")]
            self.env = {x.split("=")[0]: x.split("=")[1] for x in self.secret}

sec_man = SecMan()

def init_connection_engine(connector: Connector) -> Engine:

    if sec_man.env is not None:
        DB_USER = sec_man.env["DB_USER"]
        DB_PASS = sec_man.env["DB_PASS"]
        INSTANCE_CONNECTION_NAME = sec_man.env["INSTANCE_CONNECTION_NAME"]

    # if env var PRIVATE_IP is set to True, use private IP Cloud SQL connections
    ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") is True else IPTypes.PUBLIC
    # if env var DB_IAM_USER is set, use IAM database authentication
    user, enable_iam_auth = (
        (os.getenv("DB_IAM_USER"), True)
        if os.getenv("DB_IAM_USER")
        else (DB_USER, False)
    )

    # Cloud SQL Python Connector creator function
    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=user,
            password=DB_PASS,
            db="",
            ip_type=ip_type,
            enable_iam_auth=enable_iam_auth,
        )
        return conn

    SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn)
    return engine


# initialize Python Connector and connection pool engine
connector = Connector()
engine = init_connection_engine(connector)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()