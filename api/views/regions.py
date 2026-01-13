from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET'])
def list_regions(request):
    """List all regions with territory count"""
    query = """
    MATCH (r:Region)
    OPTIONAL MATCH (t:Territory)-[:IN_REGION]->(r)
    RETURN r.regionID AS id,
           r.regionDescription AS name,
           count(t) AS territoryCount
    ORDER BY r.regionDescription
    """
    data = Neo4jService.run(query)
    return Response(data)


@api_view(['GET'])
def get_region(request, region_id):
    """Get a single region by ID"""
    query = """
    MATCH (r:Region {regionID: $id})
    RETURN r.regionID AS id,
           r.regionDescription AS name
    """
    data = Neo4jService.run(query, {"id": int(region_id)})
    if not data:
        return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(data[0])


@api_view(['GET'])
def region_territories(request, region_id):
    """Get all territories in a region"""
    query = """
    MATCH (t:Territory)-[:IN_REGION]->(r:Region {regionID: $id})
    RETURN t.territoryID AS id,
           t.territoryDescription AS name
    ORDER BY t.territoryDescription
    """
    data = Neo4jService.run(query, {"id": int(region_id)})
    return Response(data)


@api_view(['GET'])
def list_territories(request):
    """List all territories"""
    query = """
    MATCH (t:Territory)
    OPTIONAL MATCH (t)-[:IN_REGION]->(r:Region)
    RETURN t.territoryID AS id,
           t.territoryDescription AS name,
           r.regionDescription AS region
    ORDER BY t.territoryDescription
    """
    data = Neo4jService.run(query)
    return Response(data)


@api_view(['GET'])
def get_territory(request, territory_id):
    """Get a single territory by ID"""
    query = """
    MATCH (t:Territory {territoryID: $id})
    OPTIONAL MATCH (t)-[:IN_REGION]->(r:Region)
    RETURN t.territoryID AS id,
           t.territoryDescription AS name,
           r.regionID AS regionId,
           r.regionDescription AS region
    """
    data = Neo4jService.run(query, {"id": territory_id})
    if not data:
        return Response({"error": "Territory not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(data[0])


@api_view(['GET'])
def territory_employees(request, territory_id):
    """Get all employees in a territory"""
    query = """
    MATCH (e:Employee)-[:IN_TERRITORY]->(t:Territory {territoryID: $id})
    RETURN e.employeeID AS id,
           e.firstName AS firstName,
           e.lastName AS lastName,
           e.title AS title
    ORDER BY e.lastName, e.firstName
    """
    data = Neo4jService.run(query, {"id": territory_id})
    return Response(data)
