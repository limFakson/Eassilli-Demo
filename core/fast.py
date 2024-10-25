from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, Response
from . import base, base_read
from .middleware.TokenAuthMiddleware import TokenAuthMiddleware

# Initailse fast api app
app = FastAPI()

# Add custom middleware and axcluded path
excluded_path = ["/docs", "/openapi.json", "/html"]
app.add_middleware(TokenAuthMiddleware, excluded_path=excluded_path)

# app router caller
app.include_router(base.router, prefix="/api")
app.include_router(base_read.router)


@app.get("/reload")
async def reload(request: Request):
    user = request.state.auth_user
    return {"message": f"App working nice"}


@app.get("/html")
async def test_websocket(token: str = Query(...)):
    html = (
        """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Websocket Demo</title>
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        </head>
        <body>
            <div class="container mt-3">
                <h1>FastAPI WebSocket Chat</h1>
                <h2>Your ID: <input id="ws-ids" value="""
        + token
        + """ disabled/></h2>
                <form action="" onsubmit="sendMessage(event)">
                    <input type="text" class="form-control" id="messageText" autocomplete="off"/>
                    <button class="btn btn-outline-primary mt-2">Send</button>
                </form>
                <ul id='messages' class="mt-5"></ul>
            </div>
        
            <script>
                var client_id = document.querySelector("#ws-ids").value;
                var ws = new WebSocket(`ws://localhost:8082/ws/chat?token=${client_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText");
                    ws.send(input.value);
                    input.value = '';
                    event.preventDefault();
                }
            </script>
        </body>
    </html>
    """
    )
    return HTMLResponse(content=html)
