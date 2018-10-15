<?php

//$geodaten = file_get_contents("data/geodaten", true);
$sparql =   'select ?anlage ?adresse ?lat ?long ?einspeisungsebene ?energietraeger ?leistung ?inbetriebnahmedatum ?netzbetreiber ?postleitzahl ?enr ' .
            'FROM <http://leipzig-data.de/Data/EEGAnlagenstammdaten2012/> ' .
            'FROM <http://leipzig-data.de/Data/EEGAnlagenstammdaten2012/Adressen/> ' .
            'FROM <http://leipzig-data.de/Data/GeoDaten/> ' .
            'where { ' .
            '?anlage <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://leipzig-data.de/Data/Model/c/Anlage> . ' .
            '?anlage <http://leipzig-data.de/Data/Model/Einspeisungsebene> ?einspeisungsebene . ' .
            '?anlage <http://leipzig-data.de/Data/Model/Energietraeger> ?energietraeger . ' .
            '?anlage <http://leipzig-data.de/Data/Model/installierteLeistung> ?leistung . ' .
            '?anlage <http://leipzig-data.de/Data/Model/Netzbetreiber> ?netzbetreiber . ' .
            '?anlage <http://leipzig-data.de/Data/Model/Inbetriebnahmedatum> ?inbetriebnahmedatum . ' .
            '?anlage <http://leipzig-data.de/Data/Model/PLZ> ?postleitzahl . ' .
            '?anlage <http://leipzig-data.de/Data/Model/hasENR> ?enr . ' .
            '?anlage <http://leipzig-data.de/Data/Model/hatAdresse> ?adresse . ' .
            '?adresse <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?lat . ' .
            '?adresse <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?long . ' .
            '}; Limit 3000';
            
$labelSparql =  'select ?class ?label ?type ' .
                'FROM <http://leipzig-data.de/Data/Model/> ' .
                'where { ' .
                '?class <http://www.w3.org/2000/01/rdf-schema#label> ?label . ' .
                'FILTER (langmatches(lang(?label), \"de\") || REGEX(lang(?label), \"^$\")) ' .
                'OPTIONAL {' .
                '?class <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type . ' .
                '}' .
                '} ';

switch ($_GET['s']) {
    case 'index':
        $content =  "templates/index.phtml";
        break;
     case 'bestandsaufnahme':
        $content =  "templates/bestandsaufnahme.phtml";
        break;
     case 'rechtliches':
        $content =  "templates/rechtliches.phtml";
        break;
    case 'geodaten':
        $content =  "templates/geodaten.phtml";
        break;
    case 'impressum':
        $content =  "templates/impressum.phtml";
        break;
    default:
        $content =  "templates/index.phtml";
}

include_once "templates/layout.phtml";

?>
