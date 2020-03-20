# CSC366_TeamProject
## Group Members
 * Tyler Davis
 * Joulien Ivanov
 * Jedi Pak
 * Luke Reckard
 * Austin Bryant
## Structure
### Relational Structre
 * The relational test driver is at `src/python/test-driver-relational.py`. This will run some sample insertions into a SQLite in-memory DB.
 * The relational classes are in `src/python/entities/`. This has the classes that correspond to tables.
 * The quries for business needs are in `src/sql/relational/`.
### postgreSQL/JSONB
 * The non-relational test driver is at `src/python/test-driver-document.py`. This will run some sample insertions into a postgres DB running in AWS (we didn't bother with security).
 * The non-relational classes are in `src/python/document/`. This has the classes that correspond to tables. The JSON schemas are in respective classes.
 * The quries for business needs are in `src/sql/document/`.
## Requirements
 * `pip` requirements are in `requirements.txt`.
## Notes
### Changes from UML diagram
 * `Receipt` objects are no longer associated with an employee (we totally overlooked tips in our UML).
 * `MenuItem` and `Indgredient` now are subclasses of `Item` for invoices.
 * `AddOn` does not modify a specific `MainDish`
 