from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.services.neo4j import Neo4jService


@api_view(['GET', 'POST'])
def list_employees(request):
    """List all employees or create a new employee"""
    if request.method == 'GET':
        query = """
        MATCH (e:Employee)
        OPTIONAL MATCH (e)-[:REPORTS_TO]->(m:Employee)
        RETURN e.employeeID AS id,
               e.firstName AS firstName,
               e.lastName AS lastName,
               e.title AS title,
               e.city AS city,
               e.country AS country,
               e.hireDate AS hireDate,
               m.firstName + ' ' + m.lastName AS reportsTo
        ORDER BY e.lastName, e.firstName
        """
        data = Neo4jService.run(query)
        return Response(data)
    
    elif request.method == 'POST':
        data = request.data
        if not data.get('firstName') or not data.get('lastName'):
            return Response(
                {"error": "firstName and lastName are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get next employee ID
        id_query = "MATCH (e:Employee) RETURN max(e.employeeID) AS maxId"
        max_id_result = Neo4jService.run(id_query)
        next_id = (max_id_result[0]['maxId'] or 0) + 1
        
        query = """
        CREATE (e:Employee {
            employeeID: $employeeID,
            firstName: $firstName,
            lastName: $lastName,
            title: $title,
            titleOfCourtesy: $titleOfCourtesy,
            birthDate: $birthDate,
            hireDate: $hireDate,
            address: $address,
            city: $city,
            region: $region,
            postalCode: $postalCode,
            country: $country,
            homePhone: $homePhone,
            extension: $extension,
            notes: $notes
        })
        RETURN e.employeeID AS id, e.firstName AS firstName, e.lastName AS lastName
        """
        result = Neo4jService.run(query, {
            "employeeID": next_id,
            "firstName": data.get('firstName'),
            "lastName": data.get('lastName'),
            "title": data.get('title', ''),
            "titleOfCourtesy": data.get('titleOfCourtesy', ''),
            "birthDate": data.get('birthDate', ''),
            "hireDate": data.get('hireDate', ''),
            "address": data.get('address', ''),
            "city": data.get('city', ''),
            "region": data.get('region', ''),
            "postalCode": data.get('postalCode', ''),
            "country": data.get('country', ''),
            "homePhone": data.get('homePhone', ''),
            "extension": data.get('extension', ''),
            "notes": data.get('notes', '')
        })
        
        # Link to manager if provided
        if data.get('reportsToId'):
            Neo4jService.run("""
                MATCH (e:Employee {employeeID: $employeeID})
                MATCH (m:Employee {employeeID: $managerId})
                CREATE (e)-[:REPORTS_TO]->(m)
            """, {"employeeID": next_id, "managerId": int(data.get('reportsToId'))})
        
        return Response(result[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def get_employee(request, employee_id):
    """Get, update or delete an employee"""
    if request.method == 'GET':
        query = """
        MATCH (e:Employee {employeeID: $id})
        OPTIONAL MATCH (e)-[:REPORTS_TO]->(m:Employee)
        RETURN e.employeeID AS id,
               e.firstName AS firstName,
               e.lastName AS lastName,
               e.title AS title,
               e.titleOfCourtesy AS titleOfCourtesy,
               e.birthDate AS birthDate,
               e.hireDate AS hireDate,
               e.address AS address,
               e.city AS city,
               e.region AS region,
               e.postalCode AS postalCode,
               e.country AS country,
               e.homePhone AS homePhone,
               e.extension AS extension,
               e.notes AS notes,
               m.employeeID AS reportsToId,
               m.firstName + ' ' + m.lastName AS reportsTo
        """
        data = Neo4jService.run(query, {"id": int(employee_id)})
        if not data:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data[0])
    
    elif request.method == 'PUT':
        data = request.data
        query = """
        MATCH (e:Employee {employeeID: $id})
        SET e.firstName = $firstName,
            e.lastName = $lastName,
            e.title = $title,
            e.titleOfCourtesy = $titleOfCourtesy,
            e.birthDate = $birthDate,
            e.hireDate = $hireDate,
            e.address = $address,
            e.city = $city,
            e.region = $region,
            e.postalCode = $postalCode,
            e.country = $country,
            e.homePhone = $homePhone,
            e.extension = $extension,
            e.notes = $notes
        RETURN e.employeeID AS id, e.firstName AS firstName, e.lastName AS lastName
        """
        result = Neo4jService.run(query, {
            "id": int(employee_id),
            "firstName": data.get('firstName', ''),
            "lastName": data.get('lastName', ''),
            "title": data.get('title', ''),
            "titleOfCourtesy": data.get('titleOfCourtesy', ''),
            "birthDate": data.get('birthDate', ''),
            "hireDate": data.get('hireDate', ''),
            "address": data.get('address', ''),
            "city": data.get('city', ''),
            "region": data.get('region', ''),
            "postalCode": data.get('postalCode', ''),
            "country": data.get('country', ''),
            "homePhone": data.get('homePhone', ''),
            "extension": data.get('extension', ''),
            "notes": data.get('notes', '')
        })
        if not result:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Update manager relationship if provided
        if data.get('reportsToId'):
            Neo4jService.run(
                "MATCH (e:Employee {employeeID: $id})-[r:REPORTS_TO]->() DELETE r",
                {"id": int(employee_id)}
            )
            Neo4jService.run("""
                MATCH (e:Employee {employeeID: $employeeID})
                MATCH (m:Employee {employeeID: $managerId})
                CREATE (e)-[:REPORTS_TO]->(m)
            """, {"employeeID": int(employee_id), "managerId": int(data.get('reportsToId'))})
        
        return Response(result[0])
    
    elif request.method == 'DELETE':
        check_query = "MATCH (e:Employee {employeeID: $id}) RETURN e"
        exists = Neo4jService.run(check_query, {"id": int(employee_id)})
        if not exists:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        query = """
        MATCH (e:Employee {employeeID: $id})
        DETACH DELETE e
        """
        Neo4jService.run(query, {"id": int(employee_id)})
        return Response({"message": "Employee deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def employee_orders(request, employee_id):
    """Get all orders sold by an employee"""
    query = """
    MATCH (e:Employee {employeeID: $id})-[:SOLD]->(o:Order)
    MATCH (c:Customer)-[:PURCHASED]->(o)
    RETURN o.orderID AS orderId,
           o.orderDate AS orderDate,
           o.shippedDate AS shippedDate,
           c.companyName AS customer
    ORDER BY o.orderDate DESC
    LIMIT 50
    """
    data = Neo4jService.run(query, {"id": int(employee_id)})
    return Response(data)


@api_view(['GET'])
def employee_territories(request, employee_id):
    """Get territories assigned to an employee"""
    query = """
    MATCH (e:Employee {employeeID: $id})-[:IN_TERRITORY]->(t:Territory)
    OPTIONAL MATCH (t)-[:IN_REGION]->(r:Region)
    RETURN t.territoryID AS id,
           t.territoryDescription AS name,
           r.regionDescription AS region
    ORDER BY t.territoryDescription
    """
    data = Neo4jService.run(query, {"id": int(employee_id)})
    return Response(data)


@api_view(['GET'])
def employee_subordinates(request, employee_id):
    """Get employees who report to this employee"""
    query = """
    MATCH (e:Employee)-[:REPORTS_TO]->(m:Employee {employeeID: $id})
    RETURN e.employeeID AS id,
           e.firstName AS firstName,
           e.lastName AS lastName,
           e.title AS title
    ORDER BY e.lastName, e.firstName
    """
    data = Neo4jService.run(query, {"id": int(employee_id)})
    return Response(data)
