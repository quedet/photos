import { Controller } from "@hotwired/stimulus";
import Cookie from "js-cookie";

export default class extends Controller {
  static values = {
    url: String,
  };

  connect() {
    const fileSelectorInput = document.querySelector('.file--selector--input');
    const dropArea = document.querySelector('.drop--section');

    fileSelectorInput.onchange = () => {
      [...fileSelectorInput.files].forEach((file) => {
        if (this.typeValidation(file.type)) {
          this.uploadFile(file);
        }
      });
    };

    dropArea.ondragover = (e) => {
      e.preventDefault();
      [...e.dataTransfer.items].forEach(item => {
        if (this.typeValidation(item.type)) {
          dropArea.classList.add('active');
        }
      });
    };


    dropArea.ondragleave = () => {
      dropArea.classList.remove('active');
    };

    dropArea.ondrop = (e) => {
      e.preventDefault();
      dropArea.classList.remove('active');

      if (e.dataTransfer.items) {
        [...e.dataTransfer.items].forEach((item) => {
          if (item.kind == 'file') {
            const file = item.getAsFile();
            if (this.typeValidation(file.type)) {
              this.uploadFile(file);
            }
          }
        });
      } else {
        [...e.dataTransfer.files].forEach((file) => {
          if (this.typeValidation(file.name)) {
            this.uploadFile(file);
          }
        });
      }
    };
  }

  typeValidation(type) {
    let splitType = type.split('/')[0];

    if (splitType === 'image') {
      return true;
    }
  }

  uploadFile(file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);

    const listSection = document.querySelector('.list--section');
    const listContainer = document.querySelector('.list');

    const csrftoken = Cookie.get('csrftoken');
    const url = `${window.location.protocol}//${window.location.host}` + this.urlValue;

    listSection.style.display = "block";
    let li = document.createElement('li');
    li.classList.add('in-prog');
    
    reader.onloadend = () => {
      li.innerHTML = `
        <div class="col">
          <img src="${reader.result}" alt="${file.name}" class="w-full">
        </div>
        <div class="col">
          <div class="file--name">
            <div class="name">${file.name}</div>
            <span>50%</span>
          </div>
          <div class="file--progress">
            <span></span>
          </div>
          <div class="file--size">
            ${(file.size/(1024*1024)).toFixed(2)} MB
          </div>
        </div>
        <div class="col">
          <svg xmlns="http://www.w3.org/2000/svg" class="cross" width="15" height="15" viewBox="0 0 15 15"><path fill="currentColor" fill-rule="evenodd" d="M12.854 2.854a.5.5 0 0 0-.708-.708L7.5 6.793L2.854 2.146a.5.5 0 1 0-.708.708L6.793 7.5l-4.647 4.646a.5.5 0 0 0 .708.708L7.5 8.207l4.646 4.647a.5.5 0 0 0 .708-.708L8.207 7.5l4.647-4.646Z" clip-rule="evenodd"/></svg>
          <svg xmlns="http://www.w3.org/2000/svg" class="tick" width="15" height="15" viewBox="0 0 15 15"><path fill="currentColor" fill-rule="evenodd" d="M14.707 3L5.5 12.207L.293 7L1 6.293l4.5 4.5l8.5-8.5l.707.707Z" clip-rule="evenodd"/></svg>
        </div>
      `;
      listContainer.prepend(li);
    };

    let http = new XMLHttpRequest();
    let data = new FormData();
    data.append('source', file);

    http.onload = () => {
      li.classList.add('complete');
      li.classList.remove('in-prog');
    };

    http.upload.onprogress = (e) => {
      let percent_complete = (e.loaded / e.total) * 100;
      console.log(percent_complete);
      li.querySelectorAll('span')[0].innerHTML = Math.round(percent_complete) + '%';
      li.querySelectorAll('span')[1].style.width = percent_complete + '%';
    };

    http.open('POST', url, true);
    http.setRequestHeader('X-CSRFToken', csrftoken);
    http.send(data);
  }
}