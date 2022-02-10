from db import ConnectingSQL
import logging

logger = logging.getLogger(__name__)


def main():
    """Create Genomes Database Table"""
    mydb = ConnectingSQL()
    mydb.execute(
        "CREATE TABLE IF NOT EXISTS genomes ("
        "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "file_name VARCHAR(100) NOT NULL,"
        "file_body TEXT NOT NULL,"
        "UNIQUE KEY(file_name)"
        ");",
        'coding_challenge'
    )
    logger.info("Successfully created genomes table")
    mydb.commit()
    mydb.close()


if __name__ == "__main__":
    main()
