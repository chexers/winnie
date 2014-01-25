import random

from datetime import datetime
from sqlobject import *

from winnie import settings

from types import *

import simplejson

sqlhub.processConnection = connectionForURI(settings.DATABASE)

def sql_debug(set=True):
    sqlhub.processConnection.debug = set

class WinnieObject(object):
    """
    A pseudo model type object to use in non-database places
    """
    def __init__(self, **kwargs):
        self.dict={}
        for arg in kwargs:
            self.dict[arg]=kwargs[arg]

    def __getattr__(self, key):
        return self.dict[key] if key in self.dict else self.__dict__[key]

    def as_dict(self):
        return self.dict

class WinnieList(object):
    """
    Something to interact with the list of items
    """

    class model(WinnieObject):
        pass

    @staticmethod
    def get(id):
        '''
        Doesn't do anything yet
        '''
        return id

class WinnieSQLObject(SQLObject):
    """
    Provides a few convenience methods for the models
    """
    def as_dict(self):
        dict = {}
        for item in self._reprItems():
            value = self.__getattribute__(item[0])
            dict[item[0]] = value if 'isoformat' not in dir(value) else value.isoformat()
        return dict

    def as_json(self):
        return simplejson.dumps(self.as_dict())

    def ref(self):
        return self.id

class intelligence(WinnieSQLObject):
    """
    A phrase learned, piece of intelligence
    """
    searchQuery = 'call search_intelligence("%s", %s);'

    class sqlmeta:
        fromDatabase = True

    def _get_score(self):
        return self._score

    def _set_score(self, value):
        self._score = value

    def _get_original(self):
        return self.message

    def _set_original(self, value):
        pass

    def use(self):
        self.lastused = datetime.now()
        return self.message

class fake_intel:
    def __init__(self,msg="No intelligence supplied."):
        self.msg = msg
    def use(self):
        print self.msg
        return None

class karma(WinnieSQLObject):
    """
    Voting for terms
    """
    class sqlmeta:
        fromDatabase = True


class account(WinnieSQLObject):
    """
    Represents a user's presence in the system
    """
    class sqlmeta:
        fromDatabase = True

class account_mask(WinnieSQLObject):
    """
    Any nickmasks seen.
    """
    account = ForeignKey('account')

    def _get_trusted(self):
        if self.account != None:
            return self.account.trusted
        else:
            return False

    def _set_trusted(self, value):
        pass

    class sqlmeta:
        fromDatabase = True

def search_intelligence(query, limit=0, lastused=60):
    """
    Called the stored procedure to search for a phrase against the db
    """
    if type(query) == StringType:
        query = (query,)

    if type(query) not in (ListType, TupleType):
        return fake_intel("Your fucking query wasn't a list or tuple")

    results = []
    for searchphrase in query:
        searchphrase = searchphrase.replace('\\', '\\\\').replace("'", "\\'")
        results.extend(
            sqlhub.processConnection.queryAll(
                intelligence.searchQuery % (searchphrase, lastused)
            )
        )

    intel = [intel_for_result(result) for result in (results if (limit == 0 or limit > len(results)) else results[0:limit])]
    error = fake_intel("Intel was empty")

    return (intel[0] if limit is 1 else intel) if intel else (error if limit is 1 else [error])
    #TODO refactor

def intel_for_result(result):
    intel = intelligence.get(result[0])
    intel.score = result[1]
    return intel