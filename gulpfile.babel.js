import gulp from 'gulp';
import sass from 'gulp-sass';
import postCSS from 'gulp-postcss';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';
import cleanCSS from 'gulp-clean-css';

sass.compiler = require('node-sass');

const paths = {
  scss: {
    src: 'assets/scss/styles.scss',
    dest: 'static/css',
  },
};

export const scss = () =>
  gulp
    .src(paths.scss.src)
    .pipe(sass().on('error', sass.logError))
    .pipe(postCSS([tailwindcss(), autoprefixer({ cascade: false })]))
    .pipe(cleanCSS())
    .pipe(gulp.dest(paths.scss.dest));
