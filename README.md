# Telegram Agent - Circle DXB

## API Server Setup

This project now includes a **FastAPI** server to expose Telegram automation features as REST endpoints.

### 1. Install Requirements

```bash
/Users/Kato/Desktop/telegram-agent/.venv/bin/python -m pip install -r requirements.txt
```

### 2. Run the Server

```bash
/Users/Kato/Desktop/telegram-agent/.venv/bin/python server.py
```

The server will start at `http://0.0.0.0:8000`.

### 3. API Documentation

Once the server is running, open your browser and go to:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

This provides an interactive Swagger UI where you can test all endpoints:

* **POST /groups**: Create a new group.
* **PUT /groups/{id}**: Rename a group.
* **DELETE /groups/{id}**: Delete a group.
* **POST /contacts**: Add a contact.
* **DELETE /contacts/{id}**: Remove a contact.
* **POST /messages/scrape**: Scrape messages from a chat.

### 4. Deployment

To deploy, simply push this code to your server. Ensure you:

1. Install python dependencies.
2. **Important**: You must generate the `circle_dxb_session.session` file locally (by running `main.py` once) and upload it to the server, OR run `main.py` on the server once to authenticate interactively.
3. Run `server.py` (or use a process manager like `supervisor` or `systemd`).
