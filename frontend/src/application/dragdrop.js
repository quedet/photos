// const dropArea = document.querySelector('.drop--section');
// const listSection = document.querySelector('.list--section');
// const listContainer = document.querySelector('.list');
const fileSelector = document.querySelector('.file--selector');
const fileSelectorInput = document.querySelector('.file--selector--input');

fileSelector.onlick = () => fileSelectorInput.click();
fileSelectorInput.onchange = () => {
  [...fileSelectorInput.files].forEach((file) => {
    if (typeValidation(file.type)) {
      console.log(file);
    }
  });
};

function typeValidation(type) {
  let splitType = type.split('/')[0];

  if (splitType === 'image') {
    return true;
  }
}