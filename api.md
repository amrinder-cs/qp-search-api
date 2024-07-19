# API Documentation

The parameters are query parameters, usage example:

http://localhost:6969/subjects?branchId=1&scheme=2018&semester=1

## QP Search Endpoint

### URL

GET /qp-search [now replaced by /search-papers, see below]


### Parameters

- `q` (required): The search query.

### Description

> This endpoint allows you to search for files by their names using a case-insensitive search.

## Search Papers Endpoint

### URL

GET /search-papers


### Parameters

- `paperId`: The ID of the paper.
- `mCode`: The M code.
- `subjectCode`: The code of the subject.

### Description

> This endpoint allows you to search for exam papers based on the paper ID, M code, or subject code. You may pass all of them at once


## QP Branches Endpoint

### URL

GET /qp-branches


### Description

> This endpoint retrieves a list of branches along with their IDs.


## Subjects Endpoint

### URL

GET /subjects


### Parameters

- `branchId` (required): The ID of the branch.
- `scheme` (required): The scheme.
- `semester` (required): The semester.

### Description

> This endpoint retrieves a list of subjects based on the provided branch ID, scheme, and semester.
