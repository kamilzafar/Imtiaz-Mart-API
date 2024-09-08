# Imtiaz Mart API

This project implements an Online Mart API using an event-driven microservices architecture. The system is designed to handle high volumes of transactions, ensuring scalability, maintainability, and efficiency. It leverages FastAPI for API development, Kafka for event streaming, and a range of modern technologies for cloud deployment.

## Project Overview

The Imtiaz Mart API is built using an event-driven microservices architecture. Each microservice handles a specific domain, such as user management, product catalog, order processing, and payments. The services communicate asynchronously through Kafka, ensuring real-time data flow and scalability.

## Key Features

- **Microservices Architecture**: Each domain (User, Product, Order, Payment, etc.) is managed by an independent microservice.
- **Event-Driven**: Kafka is used for asynchronous communication between services.
- **API Gateway**: Kong is used to manage routing, authentication, and rate-limiting.
- **CI/CD**: Automated with GitHub Actions, ensuring reliable and consistent deployment.

## Technologies Used

- **FastAPI**: High-performance web framework for building APIs.
- **Docker**: Containerization for consistent environments across different stages.
- **Kafka**: Event streaming platform for real-time communication between services.
- **PostgreSQL**: Database management with each microservice having its own instance.
- **Protocol Buffers (Protobuf)**: Efficient data serialization for messages exchanged between services.
- **Kong**: API Gateway for managing and routing API requests.
- **Azure Container Apps**: Cloud deployment with scalability.
- **GitHub Actions**: CI/CD pipeline automation.
- **Test-Driven Development (TDD)**: Ensuring code quality with Pytest.
- **Behavior-Driven Development (BDD)**: Aligning code functionality with business requirements using Behave.

## Architecture

- **Microservices**: Services include User, Product, Order, Inventory, Notification, and Payment services.
- **Event-Driven Communication**: Kafka acts as the event bus. Protobuf defines the message structure for inter-service communication.
- **Data Storage**: PostgreSQL databases for persistence with a database-per-service pattern.
- **API Gateway**: Managed by Kong, handling routing and other cross-cutting concerns.

## Deployment

- **Azure Container Apps**: Scalable cloud deployment using Azure Container Apps and Azure Container Registry.
- **CI/CD with GitHub Actions**: Continuous deployment triggered on each commit, ensuring code quality by running tests before deployment.

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/kamilzafar/Imtiaz-Mart-API.git
   cd Imtiaz-Mart-API

2. Set up the development environment using DevContainers.
3. Use Docker Compose to orchestrate microservices and dependencies.

   ```bash
   docker compose --profile database up 
