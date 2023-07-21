import { Controller } from "@hotwired/stimulus";
import Cropper from "cropperjs";
import "cropperjs/dist/cropper.min.css";

export default class extends Controller {
  static targets = ['image', 'result', 'zoomButton'];
  static values = {
    zoom: {
      type: Boolean,
      default: false
    }
  };

  connect() {
    this.zoomButtonTarget.addEventListener("click", () => {
      if (this.zoomValue == true) {
        this.zoomValue = false;
      } else {
        this.zoomValue = true;
      }
    });
  }

  zoomValueChanged(newVal) {
    console.log(newVal);
    const options = {
      dragMode: 'crop',
      preview: '.detail--preview',
      viewMode: 2,
      modal: true,
      background: false,
    };
    
    if (newVal === true) {
      // this.resultTarget.classList.remove("hidden");
      new Cropper(this.imageTarget, options);
    } else {
      // this.resultTarget.classList.add("hidden");
    }
  }
}