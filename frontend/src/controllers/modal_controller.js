import { Modal } from "tailwindcss-stimulus-components";

export default class extends Modal {
  static targets = [...Modal.targets, ...['modalContent']];
  static values = {
    ...Modal.values,
    ...{
      url: String,
    }
  };

  open(e) {
    this.loadContents();
    super.open(e);
  }

  close(e) {
    if (this.hasModalContentTarget) {
      const frame = this.modalContentTarget;
      frame.innerHTML = '';
    }
    super.close(e);
  }

  loadContents() {
    if (this.hasModalContentTarget && this.hasUrlValue) {
      const frame = this.modalContentTarget;

      let reloadFlag = false;
      if (frame.src === this.urlValue) {
        reloadFlag = true;
      }
      frame.src = this.urlValue;

      if (reloadFlag) {
        frame.reload();
      }
    }
  }
}