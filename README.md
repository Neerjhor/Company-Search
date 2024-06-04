# Company Search

## Installation

**With python**

```shell
$ git clone https://github.com/Neerjhor/Company-Search.git
$ cd Company_Search
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip3 install -r requirements.txt
$ python run.py
```

## Description

This models a hierarchy of companies in a database. Each company has a name and has only one parent company. It is possible to assign users to a company at any level of the hierarchy. It is also possible for a user to search for companies by name. Elasticsearch is used to store the search index.

The search functionality implements a method of access control which only allows the company that the user is assigned to and its descendants in the hierarchy to appear in the search results.

Some companies and some users are seeded when the application is run. The routes operate based on them.

You can see a nice interactive documentation if you go to `http://127.0.0.1:8000/docs` after running the application.

## API Usage

### List the descendants for a provided <company_id>

**Definition**

`GET /companies/{company_id}/descendants`

Will fetch all descendants of the company (including the company).

**Response**

- `200 OK` on success

```json
[
  {
    "name": "Company_A",
    "parent_id": null,
    "id": 1
  },
  {
    "name": "Company_B",
    "parent_id": 1,
    "id": 2
  },
  {
    "name": "Company_C",
    "parent_id": 1,
    "id": 3
  }
]
```

- `404 NOT_FOUND` on failure on non-existent company

```json
{
    "detail" : "Company does not exist.",
}
```

### List the companies with a partial or full name match with the query \<q\>

**Definition**

`GET /users/{user_id}/companies?q=<query>`

Accepts a search term and returns all companies with a partial or full name match, which the authenticated user should be able to see according to the access control rules described above.

**Response**

- `200 OK` on success

```json
[
  {
    "name": "Company_B",
    "parent_id": 1,
    "id": 2
  },
  {
    "name": "Company_C",
    "parent_id": 1,
    "id": 3
  }
]
```

## Using the endpoints with `curl`

### List the descendants for a provided <company_id>

```
curl -X 'GET' \
  'http://127.0.0.1:8000/companies/1/descendants' \
  -H 'accept: application/json'
```

### List the companies with a partial or full name match with the query \<q\>

```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/2/companies?q=Company' \
  -H 'accept: application/json'
```

## Future Work

- API endpoints for creating companies and users should be introduced.
- Authentication and authorization should be implemented for users, before fetching search results.
- We can add some healthcheck and monitoring.
- We can add a cache if the user base grows.
- We can use https for more security.