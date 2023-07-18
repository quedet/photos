import "@hotwired/turbo";
import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Lightbox from "stimulus-lightbox";
import 'lightgallery/css/lightgallery.css';

window.Stimulus = Application.start();
const context = require.context("../controllers", true, /\.js$/);
window.Stimulus.load(definitionsFromContext(context));
window.Stimulus.register('lightbox', Lightbox);
