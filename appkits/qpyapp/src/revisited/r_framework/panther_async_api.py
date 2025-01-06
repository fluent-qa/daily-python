
from datetime import datetime, timedelta

from panther import status, Panther
from panther.app import GenericAPI
from panther.response import Response


class FirstAPI(GenericAPI):
    # Cache Response For 10 Seconds
    cache = True
    cache_exp_time = timedelta(seconds=10)

    def get(self):
        date_time = datetime.now().isoformat()
        data = {'detail': f'Hello World | {date_time}'}
        return Response(data=data, status_code=status.HTTP_202_ACCEPTED)


url_routing = {'': FirstAPI}
app = Panther(__name__, configs=__name__, urls=url_routing)



from panther import Panther
from panther.app import GenericAPI
from panther.response import HTMLResponse
from panther.websocket import GenericWebsocket


class FirstWebsocket(GenericWebsocket):
    async def connect(self, **kwargs):
        await self.accept()

    async def receive(self, data: str | bytes):
        await self.send(data)


class MainPage(GenericAPI):
    def get(self):
        template = """
        <input type="text" id="messageInput">
        <button id="sendButton">Send Message</button>
        <ul id="messages"></ul>
        <script>
            var socket = new WebSocket('ws://127.0.0.1:8000/ws');
            socket.addEventListener('message', function (event) {
                var li = document.createElement('li');
                document.getElementById('messages').appendChild(li).textContent = 'Server: ' + event.data;
            });
            function sendMessage() {
                socket.send(document.getElementById('messageInput').value);
            }
            document.getElementById('sendButton').addEventListener('click', sendMessage);
        </script>
        """
        return HTMLResponse(template)

url_routing = {
    '': MainPage,
    'ws': FirstWebsocket,
}
app = Panther(__name__, configs=__name__, urls=url_routing)
