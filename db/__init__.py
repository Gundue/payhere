from platform import platform

DB_ID = "root"
DB_PW = "1234"
DB_HOST = "127.0.0.1" if "Windows" in platform() else "host.docker.internal"
DB_PORT = 3306
DB = "cafe"
TEST_DB = "cafe_test"