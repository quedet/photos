import { Controller } from "@hotwired/stimulus";
// import Masonry from "masonry-layout";

export default class extends Controller {
  static targets = ['grid'];

  connect() {
    
    // new Masonry(this.gridTarget, {
    //   itemSelector: '.grid-item',
    //   gutter: 5,
    //   // columnWidth: 200,
    //   percentPosition: true
    // });

    console.log(this.gridTarget);
  }
}