1. Login

```bash
http://localhost:8000/login
```

Credenciales: {"username":"user1", "password":"pass1"}

Me devuelve;

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.2d3sH1n0aY5lStuwLcJrYKHx3m4amfqS2RRAib-gStE"
}

2. Conectamos

ws://localhost:8000/ws?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.2d3sH1n0aY5lStuwLcJrYKHx3m4amfqS2RRAib-gStE


3. WSS

make run-ssl

https://localhost:8000/login

wss://localhost:8000/ws?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.2d3sH1n0aY5lStuwLcJrYKHx3m4amfqS2RRAib-gStE

![alt text](image.png)