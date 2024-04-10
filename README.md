<h1 align='center'> Quest-Room </h1>

<p align='center'> Create chat rooms and solve problems with friends 
<br> The member with maximum point wins 🚀
</p> 

<p align='center'>
    <img alt="Python" src="https://img.shields.io/badge/python-356f9f?style=for-the-badge&logo=python&logoColor=ffdd54" />
    <img alt="Javascript" src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=JavaScript&logoColor=black&style=for-the-badge" />
    <img alt="Django" src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=fff&style=for-the-badge" />
    <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white&style=for-the-badge" /><br>
    <img alt="Redis" src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" />
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

## About 💡
The project is currently in development but majority of the chat room feature have been added.
The project is built using Django and Django Channels for real-time chat feature. Redis is used as a channel layer for Django Channels. It uses Websockets for real-time communication between the server and the client with Postgres as the database.

## Technologies Used 🚀
The Quest room website utilizes the following technologies:

- [Django](https://www.djangoproject.com/): The main web framework.
- [Django Channels](https://github.com/django/channels): The WebSocket framework.
- [Celery](http://www.celeryproject.org/): An asynchronous task queue.
- [Redis](https://redis.io/): A message broker and cache backend.
- [Daphne](https://github.com/django/daphne): An HTTP and WebSocket protocol server.
- [Docker](https://www.docker.com): Lightweight Container Management

## Deployment ✨
### Docker 🐋
To deploy the application using Docker, follow these steps:<br>
Before following these steps, make sure you have docker installed. Get docker [here](https://www.docker.com/get-started/).
1. Clone the repository.
2. Build and run the project with `docker compose up --build`
3. Visit `http://localhost:8000/` in your web browser.
