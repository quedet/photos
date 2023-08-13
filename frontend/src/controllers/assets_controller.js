import { Controller } from "@hotwired/stimulus";
import { connectStreamSource, disconnectStreamSource } from "@hotwired/turbo";
import ReconnectingWebSocket from 'reconnecting-websocket'; 

export default class extends Controller {
  static targets = ['button'];

  static values = {
    socketUrl: String
  };

  connect() {
    const ws_url = this.socketUrlValue;
    this.source = new ReconnectingWebSocket((window.location.protocol === 'https:'? 'wss': 'ws') + "://" + window.location.host + ws_url);
    connectStreamSource(this.source);

    if (this.buttonTargets) {
      this.buttonTargets.forEach(element => {
        element.onclick = () => {
          const newData = {
            "action": "favorite",
            "data": {
              "id": element.dataset.id
            }
          };
  
          this.SendData(newData, this.source);
        };
      });
    }
  }

  disconnect() {
    if (this.source) {
      disconnectStreamSource(this.source);
      this.source.close();
      this.source = null;
    }
  }
  /**
   * Send data to websockets server
   * @param {String} data
   * @param {WebSocket} webSocket
   * @return {void}
   */
  SendData(data, webSocket) {
    webSocket.send(JSON.stringify(data));
  }
}