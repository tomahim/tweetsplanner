# Tweet Planner tool

Tweets Planner intends to provide a smart dashboard to plan tweets. 

This project is a demo application with the usage of various tools together :

- Front-end : ReactJS
- Back-end : Flask 
- Database : PostgresSQL
- Other : Docker, Twitter API

### Pre-requirements

- Docker
- A Twitter Developer account and a registered application

### Configure / Run the application

First, you will need to provide the twitter credentials of your application.

See the template file [twitter-credentials.template.py](backend/twitter-credentials.template.py)

Then, all you have to do is run the application by using this command :

```
docker-compose up --build
```

### Features roadmap

- [X] Being able to launch ReactJS, Flask and PostgreSQL using Docker
- [X] Basic Login / registration feature (with JWT support) 
- [ ] Create a CRUD dashboard to plan tweets --> IN PROGRESS
- [ ] Use Twitter API to automatically send tweets
- [ ] Add unit tests
