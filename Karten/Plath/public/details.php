<?php
/**
 * User: Immanuel Plath
 * Date: 18.12.14
 */

// load app settings
//=========================
include_once "../config/config.php";

// debug settings
//=========================
if ($settings["debug"] == "1") {
    error_reporting(E_ALL);
} else {
    error_reporting(0);
}

// include section
//=========================
include_once "../module/translate.php";
include_once "../module/getDetails.php";

// ouput settings
//=========================
ini_set('default_charset', 'utf-8');

// Local Function: Return json encoded result of getLocationDetails
// param: search string
// return: JSON object
//=========================
function outDetails($uri)
{
    return getLocationDetails($uri, getLanguage());
}

// print search result as JSON object to the user
if (!empty($_GET["uri"])) { echo outDetails($_GET["uri"]); }

// echo outDetails("Nachtleben"); // to test it

?>



