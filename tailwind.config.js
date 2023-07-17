/** @type {import('tailwindcss').Config} */
const path = require('path');

const pySitePackages = path.join(__dirname, '.venv/Lib/site-packages');

const projectPaths = [
  path.join(__dirname, 'server/templates/**/*.html'),
];

let pyPackagesPaths = [];

if (pySitePackages) {
  pyPackagesPaths = [
    path.join(pySitePackages, "./crispy_tailwind/**/*.html"),
    path.join(pySitePackages, "./crispy_tailwind/**/*.py"),
    path.join(pySitePackages, "./crispy_tailwind/**/*.js"),
  ];
}
const contentPaths = [...projectPaths, ...pyPackagesPaths];

module.exports = {
  content: contentPaths,
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
