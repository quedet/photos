from channels.generic.websocket import JsonWebsocketConsumer
from apps.assets.models import Image, Favorite
from django.shortcuts import get_object_or_404

from turbo_response import TurboStream


class AssetsConsumer(JsonWebsocketConsumer):
    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()

    def html_message(self, event):
        html = event['html']
        self.send(text_data=html)

    def receive_json(self, content, **kwargs):
        data = content['data']

        match content['action']:
            case 'favorite':
                image = get_object_or_404(Image, pk=data['id'])
                user = self.scope['user']
                favorite, created = Favorite.objects.get_or_create(
                    owner=user, image=image)
                action = "Marked"
                html = TurboStream(
                    f"asset--{image.id}--button").update.template("components/blocks/unmark.html").render()

                if not created:
                    favorite.delete()
                    action = "Unmarked"
                    html = TurboStream(
                        f"asset--{image.id}--button").update.template("components/blocks/mark.html").render()

                print(action)

                self.html_message({
                    'type': 'html_message',
                    'html': html
                })
