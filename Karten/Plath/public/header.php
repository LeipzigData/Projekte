<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 11.02.2015
 *
 * The header imports translational data and provides the common header part.
 */

include_once "../module/translate.php";

// get language and menu entries from INI file
$language = getLanguage();
$translation = getTranslation($language);

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="description" content="Jugenstadtplan Leipzig"/>
    <meta name="author" content="Immanuel Plath"/>
    <link rel="icon" href="img/favicon.ico"/>

    <title><?php echo $translation["tabTitle"]; ?></title>
    
    <!-- Bootstrap core CSS -->
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
    <link href="css/flag-icon.min.css" rel="stylesheet"/>
    <!-- Custom styles for this template -->
    <link href="css/sticky-footer-navbar.css" rel="stylesheet"/>
    <link href="css/custom.css" rel="stylesheet"/>
    <!-- Include Map Css Styles -->
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
    
  </head>
<!-- end header -->