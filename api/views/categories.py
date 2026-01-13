from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_categories(request):
    """List all categories or create a new category"""
    if request.method == 'GET':
        query = """
        MATCH (c:Category)
        OPTIONAL MATCH (p:Product)-[:PART_OF]->(c)
        RETURN c.categoryID AS id,
               c.categoryName AS name,
               c.description AS description,
               count(p) AS productCount
        ORDER BY c.categoryName
        """
        data = Neo4jService.run(query)
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('categoryName'):
            return Response(
                {"error": "categoryName is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get next category ID
        id_query = "MATCH (c:Category) RETURN max(c.categoryID) AS maxId"
        max_id_result = Neo4jService.run(id_query)
        next_id = (max_id_result[0]['maxId'] or 0) + 1
        
        query = """
        CREATE (c:Category {
            categoryID: $categoryID,
            categoryName: $categoryName,
            description: $description
        })
        RETURN c.categoryID AS id, c.categoryName AS name
        """
        result = Neo4jService.run(query, {
            "categoryID": next_id,
            "categoryName": data.get('categoryName'),
            "description": data.get('description', '')
        })
        return Response(result[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_category(request, category_id):
    """Get, update or delete a category"""
    if request.method == 'GET':
        query = """
        MATCH (c:Category {categoryID: $id})
        RETURN c.categoryID AS id,
               c.categoryName AS name,
               c.description AS description
        """
        data = Neo4jService.run(query, {"id": int(category_id)})
        if not data:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (c:Category {categoryID: $id})
        SET c.categoryName = $categoryName,
            c.description = $description
        RETURN c.categoryID AS id, c.categoryName AS name
        """
        result = Neo4jService.run(query, {
            "id": int(category_id),
            "categoryName": data.get('categoryName', ''),
            "description": data.get('description', '')
        })
        if not result:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result[0])
    
    elif request.method == 'DELETE':
        check_query = "MATCH (c:Category {categoryID: $id}) RETURN c"
        exists = Neo4jService.run(check_query, {"id": int(category_id)})
        if not exists:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        query = """
        MATCH (c:Category {categoryID: $id})
        DETACH DELETE c
        """
        Neo4jService.run(query, {"id": int(category_id)})
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
