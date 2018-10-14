<?php
error_reporting(1);

set_time_limit(360);
ini_set("memory_limit", "1024M");
error_reporting(E_ALL);
ini_set('display_errors', true);

$lat = 51.3400;
$lon = 12.3800;

include_once "php/functions.php";

function preamble($lang) {
    $out='
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="de">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>Jugendstadtplan 2013</title>

    <!-- Java Scripts -->
    <script src="http://cdn.leafletjs.com/leaflet-0.5/leaflet.js" type="text/javascript"></script>
    <script src="javascript/jquery-1.10.1.min.js" type="text/javascript"></script>
    <script src="javascript/functions.js" type="text/javascript"></script>
    <script src="javascript/leaflet.awesome-markers.js" type="text/javascript"></script>

    <!-- StyleSheets -->
    <link rel="stylesheet" href="css/leaflet.css"/>
    <!--[if lte IE 8]>
    <link rel="stylesheet" href="css/leaflet.css"/>
    <link rel="stylesheet" href="css/font-awesome-ie7.min.css">
    <![endif]-->
    <link rel="stylesheet" href="css/style.css"/>
    <link rel="stylesheet" href="css/leaflet.awesome-markers.css">
    <link rel="stylesheet" href="css/font-awesome.min.css">
</head>

<body>
<div id="header">';
        if($lang=="en") {
            $out.='<a href="index.php"><img src="images/flag_de.jpg" alt="German"/></a>';
        }
        else {
            $out.='<a href="index.php?lang=en"><img src="images/flag_en.jpg" alt="English"/></a>';
        }
$out.='<img src="images/flag_fr.jpg" alt="French"/>
<input type="search"
       id="searchfield"
       onkeyup="showResult(this.value)"/>
<div id="livesearch"></div>
</div> <!-- end header -->
';
    return $out;
}

function mainPage($quelle,$lang) {
    $text_elements=getTextElements(); 
    $out='
<div id="inner-wrap">
  <div id="wrap-details">
    <div id="detailsbox"><img src="images/testpic.jpg" width="220px" alt="Testpic"/>';
    $out.='<div id="label"><a href="#" onclick="expand_divs("description")">'
        .$text_elements['Details'][4][$lang] .'</a></div>';
    $out.='<div id="description">'.$text_elements['Details'][3][$lang].'</div>';
    $out.='<div class="details_subnavi"><a href="#" onclick="expand_divs("adresse")">'
        .$text_elements['Details'][0][$lang].'</a></div>';
    $out.='<div id="adresse" style="display:none;">'.$text_elements['Details'][3][$lang].'</div>';
    $out.='<div class="details_subnavi"><a href="#" onclick="expand_divs("eigenschaften")">'
        .$text_elements['Details'][1][$lang].'</a></div>';
    $out.='<div id="eigenschaften" style="display:none;">'.$text_elements['Details'][3][$lang].'</div>';
    $out.='<div class="details_subnavi"><a href="#" onclick="expand_divs("kontakt")">'
        .$text_elements['Details'][2][$lang].'</a></div>';
    $out.='<div id="kontakt" style="display:none;">'.$text_elements['Details'][3][$lang].'</div>';
    $out.='
        </div> <!-- end detailsbox -->
      </div> <!-- end wrap-details -->
    </div> <!-- end inner-wrap -->
';
    return $out;
}

function footer($quelle,$lang) {
    return '
    <div id="footer">'.getCategories($quelle,$lang).'</div>
    <script src="javascript/global.js" type="text/javascript"></script>
<div id="filter"></div>
<?php echo "<br/>Temporärer PHP Error Log:<br/>" . $log . "<br/>" . $log2 . "<br/>" . $log3; ?>
</body>
</html>';
}

$lang="de";
// if($_REQUEST['lang']=="en"){ $lang="en";} 
$quelle='Data/unsere_data_1.json';
//echo preamble($lang).mainPage($quelle,$lang).footer($quelle,$lang);

echo getCategories($quelle,$lang);