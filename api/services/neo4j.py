from neo4j import GraphDatabase
from django.conf import settings

class Neo4jService:
    _driver = None

    @classmethod
    def driver(cls):
        if cls._driver is None:
            cls._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        return cls._driver

    @classmethod
    def run(cls, query, params=None):
        with cls.driver().session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
