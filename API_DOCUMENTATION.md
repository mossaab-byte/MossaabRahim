# 🛒 Northwind API Documentation

> **Version:** 1.0.0  
> **Base URL:** `https://your-app.onrender.com/api`  
> **Development:** `http://127.0.0.1:8000/api`

---

## 📋 Table of Contents

1. [Getting Started](#-getting-started)
2. [Authentication](#-authentication)
3. [Customers](#-customers)
4. [Products](#-products)
5. [Orders](#-orders)
6. [Suppliers](#-suppliers)
7. [Categories](#-categories)
8. [Employees](#-employees)
9. [Shippers](#-shippers)
10. [Regions & Territories](#-regions--territories)
11. [Analytics](#-analytics)
12. [Error Handling](#-error-handling)

---

## 🚀 Getting Started

### Headers Required

All requests should include these headers:

```http
Content-Type: application/json
Accept: application/json
```

### HTTP Methods

| Method | Description |
|--------|-------------|
| `GET` | Retrieve data |
| `POST` | Create new record |
| `PUT` | Update existing record |
| `DELETE` | Delete record |

### Response Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful delete) |
| `400` | Bad Request |
| `404` | Not Found |
| `500` | Server Error |

---

## 🔐 Authentication

Currently, the API is **open** (no authentication required).

```javascript
// Example fetch request
fetch('https://your-app.onrender.com/api/customers/')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 👥 Customers

### List All Customers

```http
GET /customers/
```

**Response** `200 OK`
```json
[
  {
    "id": "ALFKI",
    "name": "Alfreds Futterkiste",
    "contactName": "Maria Anders",
    "city": "Berlin",
    "country": "Germany",
    "orderCount": 6
  },
  {
    "id": "ANATR",
    "name": "Ana Trujillo Emparedados y helados",
    "contactName": "Ana Trujillo",
    "city": "México D.F.",
    "country": "Mexico",
    "orderCount": 4
  }
]
```

---

### Get Single Customer

```http
GET /customers/{customerId}/
```

**Parameters**
| Name | Type | Description |
|------|------|-------------|
| `customerId` | `string` | Customer ID (e.g., "ALFKI") |

**Response** `200 OK`
```json
{
  "id": "ALFKI",
  "name": "Alfreds Futterkiste",
  "contactName": "Maria Anders",
  "contactTitle": "Sales Representative",
  "address": "Obere Str. 57",
  "city": "Berlin",
  "region": null,
  "postalCode": "12209",
  "country": "Germany",
  "phone": "030-0074321",
  "fax": "030-0076545"
}
```

---

### Create Customer

```http
POST /customers/
```

**Request Body**
```json
{
  "customerID": "NEWCO",
  "companyName": "New Company Ltd",
  "contactName": "John Doe",
  "contactTitle": "Owner",
  "address": "123 Main Street",
  "city": "New York",
  "region": "NY",
  "postalCode": "10001",
  "country": "USA",
  "phone": "(212) 555-1234",
  "fax": "(212) 555-1235"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customerID` | `string` | ✅ Yes | Unique 5-char ID |
| `companyName` | `string` | ✅ Yes | Company name |
| `contactName` | `string` | No | Contact person |
| `contactTitle` | `string` | No | Contact's title |
| `address` | `string` | No | Street address |
| `city` | `string` | No | City |
| `region` | `string` | No | State/Region |
| `postalCode` | `string` | No | Postal code |
| `country` | `string` | No | Country |
| `phone` | `string` | No | Phone number |
| `fax` | `string` | No | Fax number |

**Response** `201 Created`
```json
{
  "id": "NEWCO",
  "name": "New Company Ltd"
}
```

---

### Update Customer

```http
PUT /customers/{customerId}/
```

**Request Body**
```json
{
  "companyName": "Updated Company Name",
  "contactName": "Jane Smith",
  "phone": "(212) 555-9999"
}
```

**Response** `200 OK`
```json
{
  "id": "NEWCO",
  "name": "Updated Company Name"
}
```

---

### Delete Customer

```http
DELETE /customers/{customerId}/
```

**Response** `204 No Content`

---

### Get Customer Orders

```http
GET /customers/{customerId}/orders/
```

**Response** `200 OK`
```json
[
  {
    "id": 10643,
    "date": "1997-08-25"
  },
  {
    "id": 10692,
    "date": "1997-10-03"
  }
]
```

---

## 📦 Products

### List All Products

```http
GET /products/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Chai",
    "unitPrice": 18.00,
    "unitsInStock": 39,
    "unitsOnOrder": 0,
    "discontinued": false,
    "category": "Beverages",
    "supplier": "Exotic Liquids"
  }
]
```

---

### Get Single Product

```http
GET /products/{productId}/
```

**Parameters**
| Name | Type | Description |
|------|------|-------------|
| `productId` | `integer` | Product ID |

**Response** `200 OK`
```json
{
  "id": 1,
  "name": "Chai",
  "unitPrice": 18.00,
  "unitsInStock": 39,
  "unitsOnOrder": 0,
  "quantityPerUnit": "10 boxes x 20 bags",
  "discontinued": false,
  "category": "Beverages",
  "categoryId": 1,
  "supplier": "Exotic Liquids",
  "supplierId": 1
}
```

---

### Create Product

```http
POST /products/
```

**Request Body**
```json
{
  "productName": "New Product",
  "unitPrice": 29.99,
  "unitsInStock": 100,
  "unitsOnOrder": 0,
  "quantityPerUnit": "24 bottles",
  "reorderLevel": 10,
  "discontinued": false,
  "categoryId": 1,
  "supplierId": 1
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productName` | `string` | ✅ Yes | Product name |
| `unitPrice` | `number` | No | Price per unit |
| `unitsInStock` | `integer` | No | Current stock |
| `unitsOnOrder` | `integer` | No | Units on order |
| `quantityPerUnit` | `string` | No | Package description |
| `reorderLevel` | `integer` | No | Reorder threshold |
| `discontinued` | `boolean` | No | Is discontinued |
| `categoryId` | `integer` | No | Category ID |
| `supplierId` | `integer` | No | Supplier ID |

**Response** `201 Created`
```json
{
  "id": 78,
  "name": "New Product"
}
```

---

### Update Product

```http
PUT /products/{productId}/
```

**Request Body**
```json
{
  "productName": "Updated Product",
  "unitPrice": 35.00,
  "unitsInStock": 50,
  "categoryId": 2,
  "supplierId": 3
}
```

**Response** `200 OK`
```json
{
  "id": 78,
  "name": "Updated Product"
}
```

---

### Delete Product

```http
DELETE /products/{productId}/
```

**Response** `204 No Content`

---

### Get Product Orders

```http
GET /products/{productId}/orders/
```

**Response** `200 OK`
```json
[
  {
    "orderId": 10285,
    "orderDate": "1996-08-20",
    "customer": "QUICK-Stop",
    "customerId": "QUICK"
  }
]
```

---

## 🧾 Orders

### List All Orders

```http
GET /orders/
```

**Response** `200 OK`
```json
[
  {
    "id": 10248,
    "orderDate": "1996-07-04",
    "requiredDate": "1996-08-01",
    "shippedDate": "1996-07-16",
    "freight": 32.38,
    "shipCity": "Reims",
    "shipCountry": "France",
    "customer": "Vins et alcools Chevalier",
    "customerId": "VINET",
    "shipper": "Federal Shipping",
    "employee": "Steven Buchanan"
  }
]
```

---

### Get Single Order

```http
GET /orders/{orderId}/
```

**Parameters**
| Name | Type | Description |
|------|------|-------------|
| `orderId` | `integer` | Order ID |

**Response** `200 OK`
```json
{
  "id": 10248,
  "orderDate": "1996-07-04",
  "requiredDate": "1996-08-01",
  "shippedDate": "1996-07-16",
  "freight": 32.38,
  "shipName": "Vins et alcools Chevalier",
  "shipAddress": "59 rue de l'Abbaye",
  "shipCity": "Reims",
  "shipRegion": null,
  "shipPostalCode": "51100",
  "shipCountry": "France",
  "customer": "Vins et alcools Chevalier",
  "customerId": "VINET",
  "shipper": "Federal Shipping",
  "shipperId": 3,
  "employee": "Steven Buchanan",
  "employeeId": 5
}
```

---

### Create Order

```http
POST /orders/
```

**Request Body**
```json
{
  "customerId": "ALFKI",
  "employeeId": 1,
  "shipperId": 1,
  "orderDate": "2026-01-15",
  "requiredDate": "2026-01-30",
  "shipName": "Alfreds Futterkiste",
  "shipAddress": "Obere Str. 57",
  "shipCity": "Berlin",
  "shipPostalCode": "12209",
  "shipCountry": "Germany",
  "freight": 32.38
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `customerId` | `string` | ✅ Yes | Customer ID |
| `employeeId` | `integer` | No | Employee ID |
| `shipperId` | `integer` | No | Shipper ID |
| `orderDate` | `string` | No | Order date (YYYY-MM-DD) |
| `requiredDate` | `string` | No | Required date |
| `shippedDate` | `string` | No | Shipped date |
| `shipName` | `string` | No | Ship to name |
| `shipAddress` | `string` | No | Ship address |
| `shipCity` | `string` | No | Ship city |
| `shipRegion` | `string` | No | Ship region |
| `shipPostalCode` | `string` | No | Ship postal code |
| `shipCountry` | `string` | No | Ship country |
| `freight` | `number` | No | Shipping cost |

**Response** `201 Created`
```json
{
  "id": 11078
}
```

---

### Update Order

```http
PUT /orders/{orderId}/
```

**Request Body**
```json
{
  "shippedDate": "2026-01-20",
  "freight": 45.50,
  "shipCity": "Munich"
}
```

**Response** `200 OK`
```json
{
  "id": 11078
}
```

---

### Delete Order

```http
DELETE /orders/{orderId}/
```

**Response** `204 No Content`

---

### Get Order Details (Line Items)

```http
GET /orders/{orderId}/details/
```

**Response** `200 OK`
```json
[
  {
    "productId": 11,
    "productName": "Queso Cabrales",
    "unitPrice": 14.00,
    "quantity": 12,
    "discount": 0,
    "lineTotal": 168.00
  },
  {
    "productId": 42,
    "productName": "Singaporean Hokkien Fried Mee",
    "unitPrice": 9.80,
    "quantity": 10,
    "discount": 0,
    "lineTotal": 98.00
  }
]
```

---

### Add Product to Order

```http
POST /orders/{orderId}/details/
```

**Request Body**
```json
{
  "productId": 11,
  "quantity": 5,
  "unitPrice": 14.00,
  "discount": 0.1
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productId` | `integer` | ✅ Yes | Product ID |
| `quantity` | `integer` | ✅ Yes | Quantity |
| `unitPrice` | `number` | No | Unit price (auto from product) |
| `discount` | `number` | No | Discount (0-1) |

**Response** `201 Created`
```json
{
  "productId": 11,
  "quantity": 5
}
```

---

## 🏭 Suppliers

### List All Suppliers

```http
GET /suppliers/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Exotic Liquids",
    "contactName": "Charlotte Cooper",
    "contactTitle": "Purchasing Manager",
    "city": "London",
    "country": "UK",
    "phone": "(171) 555-2222",
    "productCount": 3
  }
]
```

---

### Get Single Supplier

```http
GET /suppliers/{supplierId}/
```

**Response** `200 OK`
```json
{
  "id": 1,
  "name": "Exotic Liquids",
  "contactName": "Charlotte Cooper",
  "contactTitle": "Purchasing Manager",
  "address": "49 Gilbert St.",
  "city": "London",
  "region": null,
  "postalCode": "EC1 4SD",
  "country": "UK",
  "phone": "(171) 555-2222",
  "fax": null,
  "homePage": null
}
```

---

### Create Supplier

```http
POST /suppliers/
```

**Request Body**
```json
{
  "companyName": "New Supplier Inc",
  "contactName": "John Smith",
  "contactTitle": "Sales Manager",
  "address": "100 Industrial Way",
  "city": "Chicago",
  "region": "IL",
  "postalCode": "60601",
  "country": "USA",
  "phone": "(312) 555-1234"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `companyName` | `string` | ✅ Yes | Company name |
| `contactName` | `string` | No | Contact person |
| `contactTitle` | `string` | No | Contact's title |
| `address` | `string` | No | Address |
| `city` | `string` | No | City |
| `region` | `string` | No | Region |
| `postalCode` | `string` | No | Postal code |
| `country` | `string` | No | Country |
| `phone` | `string` | No | Phone |
| `fax` | `string` | No | Fax |
| `homePage` | `string` | No | Website |

**Response** `201 Created`
```json
{
  "id": 30,
  "name": "New Supplier Inc"
}
```

---

### Update Supplier

```http
PUT /suppliers/{supplierId}/
```

**Response** `200 OK`

---

### Delete Supplier

```http
DELETE /suppliers/{supplierId}/
```

**Response** `204 No Content`

---

### Get Supplier Products

```http
GET /suppliers/{supplierId}/products/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Chai",
    "unitPrice": 18.00,
    "unitsInStock": 39,
    "category": "Beverages"
  }
]
```

---

## 🏷️ Categories

### List All Categories

```http
GET /categories/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Beverages",
    "description": "Soft drinks, coffees, teas, beers, and ales",
    "productCount": 12
  },
  {
    "id": 2,
    "name": "Condiments",
    "description": "Sweet and savory sauces, relishes, spreads, and seasonings",
    "productCount": 12
  }
]
```

---

### Get Single Category

```http
GET /categories/{categoryId}/
```

**Response** `200 OK`
```json
{
  "id": 1,
  "name": "Beverages",
  "description": "Soft drinks, coffees, teas, beers, and ales"
}
```

---

### Create Category

```http
POST /categories/
```

**Request Body**
```json
{
  "categoryName": "New Category",
  "description": "Description of new category"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `categoryName` | `string` | ✅ Yes | Category name |
| `description` | `string` | No | Description |

**Response** `201 Created`
```json
{
  "id": 9,
  "name": "New Category"
}
```

---

### Update Category

```http
PUT /categories/{categoryId}/
```

**Response** `200 OK`

---

### Delete Category

```http
DELETE /categories/{categoryId}/
```

**Response** `204 No Content`

---

### Get Category Products

```http
GET /categories/{categoryId}/products/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Chai",
    "unitPrice": 18.00,
    "unitsInStock": 39
  }
]
```

---

## 👨‍💼 Employees

### List All Employees

```http
GET /employees/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "firstName": "Nancy",
    "lastName": "Davolio",
    "title": "Sales Representative",
    "city": "Seattle",
    "country": "USA",
    "hireDate": "1992-05-01",
    "reportsTo": "Andrew Fuller"
  }
]
```

---

### Get Single Employee

```http
GET /employees/{employeeId}/
```

**Response** `200 OK`
```json
{
  "id": 1,
  "firstName": "Nancy",
  "lastName": "Davolio",
  "title": "Sales Representative",
  "titleOfCourtesy": "Ms.",
  "birthDate": "1948-12-08",
  "hireDate": "1992-05-01",
  "address": "507 - 20th Ave. E.",
  "city": "Seattle",
  "region": "WA",
  "postalCode": "98122",
  "country": "USA",
  "homePhone": "(206) 555-9857",
  "extension": "5467",
  "notes": "Education includes a BA in psychology...",
  "reportsToId": 2,
  "reportsTo": "Andrew Fuller"
}
```

---

### Create Employee

```http
POST /employees/
```

**Request Body**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "title": "Sales Representative",
  "titleOfCourtesy": "Mr.",
  "birthDate": "1990-05-15",
  "hireDate": "2026-01-01",
  "address": "123 Main St",
  "city": "Seattle",
  "region": "WA",
  "postalCode": "98101",
  "country": "USA",
  "homePhone": "(206) 555-1234",
  "extension": "1234",
  "reportsToId": 2
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `firstName` | `string` | ✅ Yes | First name |
| `lastName` | `string` | ✅ Yes | Last name |
| `title` | `string` | No | Job title |
| `titleOfCourtesy` | `string` | No | Mr./Ms./Dr. |
| `birthDate` | `string` | No | Birth date |
| `hireDate` | `string` | No | Hire date |
| `address` | `string` | No | Address |
| `city` | `string` | No | City |
| `region` | `string` | No | Region |
| `postalCode` | `string` | No | Postal code |
| `country` | `string` | No | Country |
| `homePhone` | `string` | No | Phone |
| `extension` | `string` | No | Extension |
| `notes` | `string` | No | Notes |
| `reportsToId` | `integer` | No | Manager's ID |

**Response** `201 Created`
```json
{
  "id": 10,
  "firstName": "John",
  "lastName": "Doe"
}
```

---

### Update Employee

```http
PUT /employees/{employeeId}/
```

**Response** `200 OK`

---

### Delete Employee

```http
DELETE /employees/{employeeId}/
```

**Response** `204 No Content`

---

### Get Employee Orders (Sales)

```http
GET /employees/{employeeId}/orders/
```

**Response** `200 OK`
```json
[
  {
    "orderId": 10258,
    "orderDate": "1996-07-17",
    "shippedDate": "1996-07-23",
    "customer": "Ernst Handel"
  }
]
```

---

### Get Employee Territories

```http
GET /employees/{employeeId}/territories/
```

**Response** `200 OK`
```json
[
  {
    "id": "06897",
    "name": "Wilton",
    "region": "Eastern"
  }
]
```

---

### Get Employee Subordinates

```http
GET /employees/{employeeId}/subordinates/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "firstName": "Nancy",
    "lastName": "Davolio",
    "title": "Sales Representative"
  }
]
```

---

## 🚚 Shippers

### List All Shippers

```http
GET /shippers/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Speedy Express",
    "phone": "(503) 555-9831",
    "orderCount": 249
  },
  {
    "id": 2,
    "name": "United Package",
    "phone": "(503) 555-3199",
    "orderCount": 326
  }
]
```

---

### Get Single Shipper

```http
GET /shippers/{shipperId}/
```

**Response** `200 OK`
```json
{
  "id": 1,
  "name": "Speedy Express",
  "phone": "(503) 555-9831"
}
```

---

### Create Shipper

```http
POST /shippers/
```

**Request Body**
```json
{
  "companyName": "Fast Delivery Co",
  "phone": "(555) 123-4567"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `companyName` | `string` | ✅ Yes | Company name |
| `phone` | `string` | No | Phone number |

**Response** `201 Created`
```json
{
  "id": 4,
  "name": "Fast Delivery Co"
}
```

---

### Update Shipper

```http
PUT /shippers/{shipperId}/
```

**Response** `200 OK`

---

### Delete Shipper

```http
DELETE /shippers/{shipperId}/
```

**Response** `204 No Content`

---

### Get Shipper Orders

```http
GET /shippers/{shipperId}/orders/
```

**Response** `200 OK`
```json
[
  {
    "orderId": 10248,
    "orderDate": "1996-07-04",
    "shippedDate": "1996-07-16",
    "shipCity": "Reims",
    "shipCountry": "France",
    "customer": "Vins et alcools Chevalier"
  }
]
```

---

## 🌍 Regions & Territories

### List All Regions

```http
GET /regions/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Eastern",
    "territoryCount": 5
  },
  {
    "id": 2,
    "name": "Western",
    "territoryCount": 7
  }
]
```

---

### Get Single Region

```http
GET /regions/{regionId}/
```

**Response** `200 OK`
```json
{
  "id": 1,
  "name": "Eastern"
}
```

---

### Get Region Territories

```http
GET /regions/{regionId}/territories/
```

**Response** `200 OK`
```json
[
  {
    "id": "01581",
    "name": "Westboro"
  },
  {
    "id": "01730",
    "name": "Bedford"
  }
]
```

---

### List All Territories

```http
GET /territories/
```

**Response** `200 OK`
```json
[
  {
    "id": "01581",
    "name": "Westboro",
    "region": "Eastern"
  }
]
```

---

### Get Single Territory

```http
GET /territories/{territoryId}/
```

**Response** `200 OK`
```json
{
  "id": "01581",
  "name": "Westboro",
  "regionId": 1,
  "region": "Eastern"
}
```

---

### Get Territory Employees

```http
GET /territories/{territoryId}/employees/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "firstName": "Nancy",
    "lastName": "Davolio",
    "title": "Sales Representative"
  }
]
```

---

## 📊 Analytics

### Dashboard Summary

```http
GET /analytics/dashboard/
```

**Response** `200 OK`
```json
{
  "customerCount": 91,
  "productCount": 77,
  "orderCount": 830,
  "supplierCount": 29,
  "employeeCount": 9,
  "totalRevenue": 1265793.04
}
```

---

### Top Products

```http
GET /analytics/top-products/?limit=10
```

**Query Parameters**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `limit` | `integer` | 10 | Number of results |

**Response** `200 OK`
```json
[
  {
    "id": 38,
    "name": "Côte de Blaye",
    "orderCount": 24,
    "totalQuantity": 623,
    "totalRevenue": 141396.74
  }
]
```

---

### Top Customers

```http
GET /analytics/top-customers/?limit=10
```

**Response** `200 OK`
```json
[
  {
    "id": "QUICK",
    "name": "QUICK-Stop",
    "country": "Germany",
    "orderCount": 28,
    "totalSpent": 110277.31
  }
]
```

---

### Top Employees

```http
GET /analytics/top-employees/?limit=10
```

**Response** `200 OK`
```json
[
  {
    "id": 4,
    "name": "Margaret Peacock",
    "title": "Sales Representative",
    "orderCount": 156,
    "totalSales": 232890.85
  }
]
```

---

### Sales by Category

```http
GET /analytics/sales-by-category/
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "category": "Beverages",
    "orderCount": 404,
    "totalQuantity": 9532,
    "totalRevenue": 267868.18
  }
]
```

---

### Sales by Country

```http
GET /analytics/sales-by-country/
```

**Response** `200 OK`
```json
[
  {
    "country": "USA",
    "customerCount": 13,
    "orderCount": 122,
    "totalRevenue": 245584.62
  }
]
```

---

### Sales by Supplier

```http
GET /analytics/sales-by-supplier/
```

**Response** `200 OK`
```json
[
  {
    "id": 18,
    "supplier": "Aux joyeux ecclésiastiques",
    "country": "France",
    "productCount": 2,
    "totalQuantity": 623,
    "totalRevenue": 141396.74
  }
]
```

---

### Shipping Statistics

```http
GET /analytics/shipping-stats/
```

**Response** `200 OK`
```json
[
  {
    "id": 2,
    "shipper": "United Package",
    "orderCount": 326,
    "avgFreight": 67.23,
    "totalFreight": 21917.38
  }
]
```

---

### Monthly Sales

```http
GET /analytics/monthly-sales/?year=1997
```

**Query Parameters**
| Name | Type | Description |
|------|------|-------------|
| `year` | `string` | Filter by year (YYYY) |

**Response** `200 OK`
```json
[
  {
    "month": "1997-01",
    "orderCount": 85,
    "revenue": 61258.07
  },
  {
    "month": "1997-02",
    "orderCount": 79,
    "revenue": 38483.64
  }
]
```

---

## ❌ Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "error": "Error message description"
}
```

### Common Errors

#### 400 Bad Request
Missing required fields:
```json
{
  "error": "customerID and companyName are required"
}
```

#### 404 Not Found
Resource doesn't exist:
```json
{
  "error": "Customer not found"
}
```

#### 500 Internal Server Error
Server-side error:
```json
{
  "error": "Database connection failed"
}
```

---

## 💻 Code Examples

### JavaScript (Fetch)

```javascript
// GET all customers
const response = await fetch('https://your-app.onrender.com/api/customers/');
const customers = await response.json();

// POST new customer
const newCustomer = await fetch('https://your-app.onrender.com/api/customers/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    customerID: 'NEWCO',
    companyName: 'New Company'
  })
});

// PUT update customer
await fetch('https://your-app.onrender.com/api/customers/NEWCO/', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    companyName: 'Updated Company'
  })
});

// DELETE customer
await fetch('https://your-app.onrender.com/api/customers/NEWCO/', {
  method: 'DELETE'
});
```

### React (Axios)

```javascript
import axios from 'axios';

const API_URL = 'https://your-app.onrender.com/api';

// GET
const { data: customers } = await axios.get(`${API_URL}/customers/`);

// POST
const { data: newCustomer } = await axios.post(`${API_URL}/customers/`, {
  customerID: 'NEWCO',
  companyName: 'New Company'
});

// PUT
await axios.put(`${API_URL}/customers/NEWCO/`, {
  companyName: 'Updated Company'
});

// DELETE
await axios.delete(`${API_URL}/customers/NEWCO/`);
```

---

## 📝 Notes

1. **Trailing Slash**: All endpoints require a trailing slash (`/`)
2. **Date Format**: Use `YYYY-MM-DD` for all dates
3. **IDs**: Customer IDs are strings (5 chars), all others are integers
4. **Pagination**: List endpoints return max 100 items by default

---

## 📞 Support

For API issues or questions, contact the backend team.

---

**Last Updated:** January 2026
