var gulp = require('gulp');
var del = require('del');

var pug = require('gulp-pug');
var templateCache = require('gulp-angular-templatecache');
var ngAnnotate = require("gulp-ng-annotate");
var htmlify = require('gulp-angular-htmlify');
var concat = require("gulp-concat");
var sourcemaps = require("gulp-sourcemaps");
var log = require("fancy-log");
var livereload = require('gulp-livereload');
var uglify = require("gulp-uglify");
var gls = require('gulp-live-server');
var less = require('gulp-less');
var jslint = require('gulp-jslint');
var plumber = require('gulp-plumber');

var paths = {
    distDir: 'dist',
    less: 'src/less/style.less',
    config: './config.json',
    angularTemplates: 'src/angular/views/*.jade',
    angularDynTemplates: 'src/angular/views-dyn/*.jade',
    angularApp: ['src/angular/app/*.js', 'src/angular/controller/*.js'],
    pugTemplate: 'src/jade/*.jade',
    vendorLogos: 'logos/**',
    images: 'images/*',
    vendorFiles: [
        'node_modules/angular-animate/angular-animate.min.js',
        'node_modules/angular-local-storage/dist/angular-local-storage.min.js',
        'node_modules/angular-resource/angular-resource.min.js',
        'node_modules/angular-route/angular-route.js',
        'node_modules/angular/angular.min.js',
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/leaflet.markercluster/dist/MarkerCluster.Default.css',
        'node_modules/leaflet.markercluster/dist/MarkerCluster.css',
        'node_modules/leaflet.markercluster/dist/leaflet.markercluster.js',
        'node_modules/leaflet/dist/**/*.png',
        'node_modules/leaflet/dist/leaflet.css',
        'node_modules/leaflet/dist/leaflet.js',
        'node_modules/popper.js/dist/umd/popper.min.js',
        'node_modules/@fortawesome/fontawesome-free/css*/*.css',
        'node_modules/@fortawesome/fontawesome-free/webfonts*/**',
        'node_modules/angular-sanitize/angular-sanitize.min.js'
    ]
};

let loadConfig = () => {
    // Load configuration from config.json and overwrite from ../data/../config.json
    let config = require(paths.config);
    paths.configData = '../data/' + config.data + '/config.json';
    paths.dataDir = '../data/' + config.data;
    let config2 = require(paths.configData);
    return Object.assign(config, config2);
};
var config = loadConfig();

gulp.task('clean', function() {
    return del(paths.distDir);
});

gulp.task('clean-vendor', function() {
    return del(paths.distDir + '/vendor');
});

gulp.task('clean-data', function() {
    return del(paths.distDir + '/data');
});

gulp.task('clean-pug', function() {
    return del(paths.distDir + '/index.html');
});

gulp.task('vendor', ['clean-vendor'], function() {
    return gulp.src(paths.vendorFiles)
        .pipe(plumber())
        .pipe(gulp.dest(paths.distDir + '/vendor'));
});

gulp.task('copy-logos', function() {
    return gulp.src(paths.vendorLogos)
        .pipe(plumber())
        .pipe(gulp.dest(paths.distDir + '/logos'));
});

gulp.task('copy-images', function() {
    return gulp.src(paths.images)
        .pipe(plumber())
        .pipe(gulp.dest(paths.distDir + '/images'));
});

gulp.task('install-data', ['clean-data'], function() {
    let dataDir = '../data/' + config.data;
    gulp.src(dataDir + '/@(data.json|config.json)')
        .pipe(plumber())
        .pipe(gulp.dest(paths.distDir + '/data'));
    return gulp.src(dataDir + '/!(data.json|config.json|README.md|dropin){,/**}')
        .pipe(plumber())
        .pipe(gulp.dest(paths.distDir));
});

gulp.task('build-less', function() {
    return gulp.src(paths.less)
        .pipe(sourcemaps.init())
        .pipe(plumber())
        .pipe(less({
            compress: true,
            paths: [
                'node_modules/bootstrap-less/bootstrap',
                'node_modules/@fortawesome/fontawesome-free/less'
            ]
        }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(paths.distDir + "/css"))
        .pipe(livereload());
});

gulp.task('angular-app', function() {
    appscripts = gulp.src(paths.angularApp)
        .pipe(plumber())
        .pipe(sourcemaps.init())
        .pipe(ngAnnotate())
        // .pipe(uglify())
        .pipe(concat("app.min.js"))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(paths.distDir + "/js"))
        .pipe(livereload());
});

gulp.task('_angular-tmpl-copy1', function() {
    // Copy default templates to dynamic dir
    return gulp.src(paths.angularTemplates, {
            base: paths.angularTemplates
        })
        .pipe(gulp.dest(paths.angularDynTemplates));
});

gulp.task('_angular-tmpl-copy2', ['_angular-tmpl-copy1'], function() {
    // Copy overwritten templates to dynamic dir
    let dropin = '../data/' + config.data + '/dropin/*';
    return gulp.src(dropin, {
            base: dropin
        })
        .pipe(gulp.dest(paths.angularDynTemplates));
});

gulp.task('_angular-tmpl-compile', ['_angular-tmpl-copy2'], function() {
    // Compile everything
    return gulp.src(paths.angularDynTemplates)
        .pipe(plumber())
        .pipe(pug({
            locals: config
        }))
        .pipe(htmlify())
        .pipe(sourcemaps.init())
        .pipe(templateCache({
            root: "",
            standalone: false,
            module: "app"
        }))
        .pipe(uglify())
        .pipe(concat("app.tmpl.min.js"))
        .pipe(gulp.dest(paths.distDir + "/js"))
        .pipe(livereload());
});

gulp.task('_angular-tmpl-cleanup', ['_angular-tmpl-compile'], function() {
    // Cleanup created files
    return del(paths.angularDynTemplates);
});

gulp.task('angular-tmpl', ['_angular-tmpl-cleanup'], function() {
});

gulp.task('pug', ['clean-pug'], function() {
    gulp.src(paths.pugTemplate)
        .pipe(plumber())
        .pipe(pug({
            locals: config
        }).on('error', function(err) {
            console.log(err);
        }))
        .pipe(gulp.dest(paths.distDir));
});

gulp.task('lint', function() {
    return gulp.src(paths.angularApp)
        .pipe(plumber())
        .pipe(jslint())
        .pipe(jslint.reporter('stylish'));
});

gulp.task('watch-files', function() {
    livereload.listen();
    var server = gls.static('dist', 3000);
    server.start();
    gulp.watch(paths.pugTemplate, ['pug']);
    gulp.watch(paths.config, ['default']);
    gulp.watch(paths.configData, ['default']);
    gulp.watch(paths.dataDir + '/dropin/*', ['angular-tmpl']);
    gulp.watch(paths.angularTemplates, ['angular-tmpl']);
    gulp.watch(paths.angularApp, ['angular-app']);
    gulp.watch(paths.less, ['build-less']);
    gulp.watch('dist/@(index.html|!(vendor)/*)', function(file) {
        server.notify.apply(server, [file]);
    });
});

gulp.task('watch', ['watch-files', 'default']);
gulp.task('default', ['pug', 'vendor', 'copy-images', 'copy-logos', 'install-data', 'build-less', 'angular-tmpl', 'angular-app']);
