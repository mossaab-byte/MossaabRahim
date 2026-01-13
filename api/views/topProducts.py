from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services.neo4j import Neo4jService


@api_view(['GET'])
def top_products(request):
    query = """
    MATCH (:Customer)-[:PURCHASED]->(:Order)-[:ORDERS]->(p:Product)
    RETURN p.productName AS product, count(*) AS sales
    ORDER BY sales DESC
    LIMIT 10
    """
    data = Neo4jService.run(query)
    return Response(data)