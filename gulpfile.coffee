gulp = require 'gulp'
browserSync = require 'browser-sync'
stylus = require 'gulp-stylus'
coffee = require 'gulp-coffee'
rename = require 'gulp-rename'
nib = require 'nib'
uglify = require 'gulp-uglify'
del = require 'del'
{argv} = require 'yargs'


project =
  name: 'ark'
  dest: 'ark/static'
  tmp: '.tmp/assets'
styles =
  name: 'styles'
  exts: ['styl', 'css']
scripts =
  name: 'scripts'
  exts: ['coffee', 'js']
assets =
  name: 'assets'
  dirs: [styles.name, scripts.name]
  exts: [].concat(styles.exts, scripts.exts)
  glob: (bundle) ->
    if bundle
      "#{project.tmp}/#{bundle.name}/*/*.{#{bundle.exts.join(',')}}"
    else
      dirs = assets.dirs.join(',')
      exts = assets.exts.join(',')
      "#{project.name}/*/#{assets.name}/{#{dirs}}/**/*.{#{exts}}"


gulp.task 'clean', ['clean:collect']
gulp.task 'build', ['stylus', 'coffee']
gulp.task 'default', ['clean'], ->
  gulp.start 'build'

gulp.task 'watch', ['default'], ->
  gulp.start 'browser-sync'
  gulp.watch assets.glob(), ['build']


gulp.task 'collect', ->
  gulp.src assets.glob()
    .pipe rename (path) ->
      dirs = assets.dirs.join '|'
      pattern = new RegExp "([^/]+)/#{assets.name}/(#{dirs})(/[^/]+)?"
      matched = pattern.exec path.dirname
      path.dirname = "#{matched[2]}/#{matched[1]}#{matched[3] or ''}"
      path
    .pipe gulp.dest project.tmp

gulp.task 'stylus', ['collect'], ->
  options =
    use: nib()
    compress: not argv.debug
  gulp.src "#{project.tmp}/**/*.{#{styles.exts.join(',')}}"
    .pipe stylus options
    .pipe gulp.dest "#{project.dest}"
    .pipe browserSync.reload
      stream: true

gulp.task 'coffee', ['collect'], ->
  options =
    bare: true
  stream = gulp.src "#{project.tmp}/**/*.{#{scripts.exts.join(',')}}"
    .pipe coffee options
  unless argv.debug
    stream = stream.pipe uglify()
  stream.pipe gulp.dest "#{project.dest}"
    .pipe browserSync.reload
      stream: true

gulp.task 'browser-sync', ->
  browserSync
    port: 5500
    server:
      baseDir: '.tmp/wwwroot'
      routes:
        "/static": "#{project.dest}"

gulp.task 'clean:collect', (done) ->
  del [
    "#{project.tmp}/**/*.{#{assets.exts.join(',')}}",
  ], done

gulp.task 'clean:dist', (done) ->
  del [
    "#{project.dest}/**/*.{#{assets.exts.join(',')}}"
  ], done
