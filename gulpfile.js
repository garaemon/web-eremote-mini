const gulp = require('gulp');
const typescript = require('gulp-typescript');
const PolymerProject = require('polymer-build').PolymerProject;
const mergeStream = require('merge-stream');
const del = require('del');
const sourcemaps = require('gulp-sourcemaps');

gulp.task('ts:build', () => {

  const typescriptProject =
      typescript.createProject('tsconfig.json');

  gulp.src(['browser/**/*.ts', '!./node_modules/**'])
      .pipe(sourcemaps.init())
      .pipe(typescriptProject())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('./ts_build/'));
});

gulp.task('ts', ['ts:build']);

gulp.task('polymer:build', ['ts'], () => {
  const project = new PolymerProject(require('./polymer.json'));
  return mergeStream(project.sources(), project.dependencies())
  .pipe(gulp.dest('build/'));
});

gulp.task('polymer', ['polymer:build'])
gulp.task('polymer:clean', () => {
  del(['build']);
});
gulp.task('default', ['ts', 'polymer']);

gulp.task('watch', ['ts', 'polymer'], () => {
  gulp.watch(['browser/**/*.ts', 'tsconfig.json'], ['ts:build', 'polymer:build']);
  gulp.watch(['browser/**/*.html', 'index.html', 'polymer.json'], ['polymer'])
});

gulp.task('ts:clean', () => {
  del(['ts_build'])
});

gulp.task('clean', ['ts:clean', 'polymer:clean']);
