gulp = require 'gulp'
stylus = require 'gulp-stylus'
coffee = require 'gulp-coffee'
rename = require 'gulp-rename'
nib = require 'nib'
del = require 'del'
{argv} = require 'yargs'

project =
  name: 'ark'
  dest: './ark/static'
  tmp: '.tmp/assets'
styles =
  name: 'styles'
  exts: ['stylus', 'css']
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

gulp.task 'collect', ->
  gulp.src assets.glob()
    .pipe rename (path) ->
      dirs = assets.dirs.join '|'
      pattern = new RegExp "([^/]+)/#{assets.name}/(#{dirs})(/[^/]+)?"
      matched = pattern.exec path.dirname
      path.dirname = "#{matched[2]}/#{matched[1]}#{matched[3] or ''}"
      path
    .pipe gulp.dest project.tmp

gulp.task 'clean:collect', (done) ->
  del [
    "#{project.tmp}/**/*.{#{assets.exts.join(',')}}",
  ], done
