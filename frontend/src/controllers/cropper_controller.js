import { Controller } from "@hotwired/stimulus";
import Cropper from "cropperjs";
import "cropperjs/dist/cropper.min.css";

export default class extends Controller {
  static targets = ['image', 'result'];

  connect() {
    const options = {
      dragMode: 'crop',
      preview: '.detail--preview',
      viewMode: 1,
      modal: true,
      background: false
    };

    new Cropper(this.imageTarget, options);
  }
}