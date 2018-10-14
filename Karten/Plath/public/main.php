<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 11.02.2015
 */

include_once "../module/translate.php";
include_once "../module/getCategories.php";
include_once "../module/html.php";

// get language and menu entries from INI file
$language = getLanguage();
$translation = getTranslation($language);

?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Jugenstadtplan Leipzig">
    <meta name="author" content="Immanuel Plath">
    <link rel="icon" href="img/favicon.ico">

    <title><?php echo $translation["tabTitle"]; ?></title>
    
    <!-- Bootstrap core CSS -->
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link href="css/flag-icon.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="css/sticky-footer-navbar.css" rel="stylesheet">
    <link href="css/custom.css" rel="stylesheet">
    <!-- Include Map Css Styles -->
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" >
    
  </head>
<!-- end header -->

  <body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header"> 
          <!-- Whats the role of the following button element? For AT only ? -->
          <button type="button" class="navbar-toggle collapsed"
                  data-toggle="collapse" data-target="#navbar"
                  aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#"><?php echo $translation["label"]; ?></a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#"><?php echo $translation["map"]; ?></a></li> 
            <li><a href="#about"><?php echo $translation["aboutUs"]; ?></a></li> 
            <li class="disabled"><a href="#contact"><?php echo $translation["contact"]; ?></a></li> 
          </ul>
          <div class="col-sm-4 col-md-4">
          <!-- search field -->
            <form role="search" class="navbar-form">
                <div class="input-group col-xs-12">
                    <input id="searchfield" type="text" name="q" placeholder="Search" class="form-control">
                    <div class="input-group-btn">
                        <a class="btn btn-default startSearch"><i class="glyphicon glyphicon-search"></i></a>
                    </div>
                </div>
            </form>
          </div>
          <!-- language selection -->
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
                <a data-toggle="dropdown" class="dropdown-toggle" href="#">
                  <?php echo $translation["languageButton"]; ?>
                  <span class="flag-icon flag-icon-de"></span>
                  <span class="flag-icon flag-icon-gb"></span></a>
                <ul class="dropdown-menu">
                  <li><a href="main.php"><span class="flag-icon flag-icon-de"></span> Deutsch</a></li>
                  <li><a href="main.php?lang=en"><span class="flag-icon flag-icon-gb"></span> English</a></li>
                </ul>
            </li>
          </ul>
        </div><!-- navbar end -->
      </div><!-- container end -->
    </nav>

    <?php echo pageMap($translation["placeDescription"], $translation["opening"], $translation["contact"], 
	    $translation["properties"], $translation["chooseEntry"], $language); ?>
      <!-- start autogenerate the category selection row -->
      <?php echo getCategories($language,$translation["allCategories"],
            $translation["noCategorie"]); ?>  
      <!-- end autogenerate the category selection row -->
    </div> <!-- end container main page content -->

    <!-- Begin footer content -->
    <div class="footer">
      <div class="container">
        <p class="text-muted">&copy; <?php echo $translation["copyright"].' '.$translation["copyrightdate"]; ?> </p>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <!-- jquery is required for bootstrap, see http://holdirbootstrap.de/los-gehts/#download -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <!-- Latest compiled and minified bootstrap JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
    
    <!-- Custom JavaScript
    ================================================== -->
    <!-- Include leaflet Map JS -->
    <script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
    <!-- Custom JS Settings for Map -->
    <script src="js/custom-map.js"></script>
    <!-- Helper JS Functions -->
    <script src="js/helper.js"></script>
    
  </body>
</html>
