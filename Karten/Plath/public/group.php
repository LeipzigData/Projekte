<?php
/**
 * User: Immanuel Plath
 * Date: 26.12.14
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
include_once "../module/getLocationsFromCategories.php";

// ouput settings
//=========================
ini_set('default_charset', 'utf-8');

// Local Function: Return json encoded result of getLocationsByCategory
// param: search string
// return: JSON object
//=========================
function response($searchGroup)
{
    // Change Content Header
    header('Content-Type: application/json;charset=utf-8');
    return json_encode(getLocationsByCategory($searchGroup));
}

// print search result as JSON object to the user
if (!empty($_GET["group"])) { echo response($_GET["group"]); }

// echo response("Nachtleben"); // to test it

?>



