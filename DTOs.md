# Data Transfer Objects

## Characteristics:
- They contain only non-PII (non-Personally Identifiable Information) and showcases only this info to API clients
No business logic - this is because they contain only data. Used to transfer data which can be get & set.

- Most often, configure them to be immutable in order to preserve data integrity during transfer.

- If used for API request/response, should also consider making them serializable, for the sake of better transport b/w networks.

## Why use DTOs:
- Seperation of concerns b/w entities like the presentation layer and the domain model (eg.).
- Creating contracts b/w the backend API and the API client.

- Reduction of Coupling: Using these objects and the above mentioned pros, we can decouple DB changes from the business
logic or service layer. Meaning, changes in the database schema won't have impact on the business/service layer.

- **Reducing overhead in remote calls** by enabling us to transfer only necessary data.

- DTOs can encapsulate validation logic, ensuring that data entering a particular layer or component meets certain criteria 
before being processed.

- One  of the biggest reason is **Security**.
It allows us to control and limit the information that is exposed or transferred b/w different layers or components of an application.
