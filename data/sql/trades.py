from PyQt5.QtSql import QSqlDatabase
import os
from dotenv import load_dotenv


class Database:
    """

    The SQL query class for c-scientist for widget 'Analytics'.

    Uses PyQt5.QtSql.QSqlDatabase

    """

    def __init__(self, **credentials):
        """

        Parameters.

        ----------

        **credentials :
            host
                The database host address

            user
                Database username

            port
                Database port

            passwd
                Database password

            name
                Database name

        """
        load_dotenv('../../.env')
        self.db = QSqlDatabase.addDatabase('QPSQL', 'tester')

        self.db.setHostName(credentials.get('host', os.getenv('host')))
        self.db.setUserName(credentials.get('user', os.getenv('user')))
        self.db.setPort(credentials.get('port', os.getenv('port')))
        self.db.setPassword(credentials.get('passwd', os.getenv('passwd')))
        self.db.setDatabaseName(credentials.get('name', os.getenv('name')))

    def test_conn(self):
        """

        Returns.

        --------

        True
            If the connection succeeds

        False
            If the connection fails and a detailed error

        """
        try:
            if not self.db.open():
                raise Exception('Connectio failed', self.db.lastError().text())

            self.db.close()
            self.db.removeDatabase('tester')
            return True

        except Exception as e:
            print('Connection error', e)
            return False

    def portfolio(self):
        """

        None.

        -----

        """
        pass

    def by_coin(self):
        """

        None.

        -----

        """
        pass

    def highest_profit(self):
        """

        None.

        -----

        """
        pass

    def highest_loss(self):
        """

        None.

        -----

        """
        pass

    def volume(self):
        """

        None.

        -----

        """
        pass

    def net_profit(self):
        """

        None.

        -----

        """
        pass

    def holdings(self):
        """

        None.

        -----

        """
        pass

    def recent_trades(self):
        """

        None.

        -----

        """
        pass

