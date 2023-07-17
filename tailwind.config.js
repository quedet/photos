/** @type {import('tailwindcss').Config} */
const path = require('path');

const projectPaths = [
  path.join(__dirname, 'server/templates/**/*.html'),
];

const contentPaths = [...projectPaths];

module.exports = {
  content: contentPaths,
  theme: {
    extend: {},
  },
  plugins: [],
};
