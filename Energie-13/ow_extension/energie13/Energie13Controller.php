<?php

/**
 * Controller for Energie13.
 *
 * @category   OntoWiki
 * @package    OntoWiki_extensions_energie13
 * @author     Lars Eidam <larseidam@googlemail.com>
 * @copyright  Copyright (c) 2013
 * @license    http://opensource.org/licenses/gpl-license.php GNU General Public License (GPL)
 */ 
class Energie13Controller extends OntoWiki_Controller_Component
{
    
    private $_store;
    private $_translate;
    private $_ontologies;
    
    /**
     * init controller
     */     
    public function init()
    {
        parent::init();
        
        $this->_store = Erfurt_App::getInstance()->getStore();
        
        $this->_translate = $this->_owApp->translate;
        
        // get all models
        $this->_ontologies = $this->_config->ontologies->toArray();
        $this->_ontologies = $this->_ontologies['models'];
        
        // make model instances
        foreach ($this->_ontologies as $modelName => $model) {
            if ($this->_store->isModelAvailable($model['namespace'])) {
                $this->_ontologies[$modelName]['instance'] = $this->_store->getModel($model['namespace']);
            }
            $namespaces[$model['namespace']] = $modelName;
        }
    }
    
    public function indexAction()
    {
        $this->_owApp->getNavigation()->disableNavigation();
        
        $this->view->headLink()->appendStylesheet($this->_componentUrlBase .'public/css/index.css');
        $this->view->headLink()->appendStylesheet('http://cdn.leafletjs.com/leaflet-0.7.1/leaflet.css');
        $this->view->headScript()->appendFile('http://cdn.leafletjs.com/leaflet-0.7.1/leaflet.js');
        $this->view->headScript()->appendFile($this->_componentUrlBase .'public/js/index.js');
        
        $resultPlants = $this->_store->sparqlQuery(
            'select ?anlage
            where {
                ?anlage <http://leipzig-data.de/Data/Model/hatAdresse> ?adresse .
            };'
        );
        $this->view->countPlants = count($resultPlants);
        
        $resultPlantsWithGeo = $this->_store->sparqlQuery(
            'select ?anlage ?adresse ?lat ?long
            where {
            ?anlage <http://leipzig-data.de/Data/Model/hatAdresse> ?adresse .
            ?adresse <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?lat .
            ?adresse <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?long .
            } LIMIT 3000;'
        );
        $this->view->plantsWithGeo = $resultPlantsWithGeo;
        $this->view->countPlantsWithGeo = count($resultPlantsWithGeo);
        
        $resultPlantsWithoutGeo = $this->_store->sparqlQuery(
            'select ?anlage ?adresse
            where {
            ?anlage <http://leipzig-data.de/Data/Model/hatAdresse> ?adresse .
            OPTIONAL {?adresse ?p ?o} .
            Filter (!bound(?p))};'
        );
        $this->view->countPlantsWithoutGeo = count($resultPlantsWithoutGeo);
    }
    
    public function makegeoAction()
    {
        // disable layout for Ajax requests
        $this->_helper->layout()->disableLayout();
        // disable rendering
        $this->_helper->viewRenderer->setNoRender();
        
        $addresses = $this->_ontologies['EEGStammdaten2012Konfliktfrei']['instance']->sparqlQuery(
            'select ?anlageUri ?ort ?plz ?strasse ?nummer
            where {
            ?anlageUri <http://leipzig-data.de/Data/Model/Ort> ?ort .
            ?anlageUri <http://leipzig-data.de/Data/Model/PLZ> ?plz .
            ?anlageUri <http://leipzig-data.de/Data/Model/Strasse> ?strasse .
            ?anlageUri <http://leipzig-data.de/Data/Model/Nummer> ?nummer .
            } LIMIT 2000;'
        );
        $n = 1;
        foreach ($addresses as $address)
        {
            $strasse = $address['strasse'];
            $strasse = str_replace('.', '', $strasse);
            $strasse = str_replace('ß', 'ss', $strasse);
            $strasse = str_replace('ä', 'ae', $strasse);
            $strasse = str_replace('ö', 'oe', $strasse);
            $strasse = str_replace('ü', 'ue', $strasse);
            if (false === stristr('strasse', $strasse)) {
                $strasse = str_replace('str', 'strasse', $strasse);
                $strasse = str_replace('Str', 'Strasse', $strasse);
            } else {
                $strasse = $strasse;
            }
            
            $nummer = strtoupper($address['nummer']);
            
            $addressStr = $address['plz'].
                '.' .
                $address['ort'] .
                '.' .
                $strasse .
                '.' .
                $nummer;
            
            $addressStr = str_replace('..', '.', $addressStr);
            $addressStr = str_replace(' ', '', $addressStr);
            echo $n . ': ' . $address['anlageUri'] . ' ' . $addressStr . '<br />';
            $this->_ontologies['EEGStammdaten2012Adressen']['instance']->addStatement(
                $address['anlageUri'],
                'http://leipzig-data.de/Data/Model/hatAdresse', 
                array('value' => 'http://leipzig-data.de/Data/' . $addressStr, 'type' => 'uri')
           );
            $n++;
        }
    }
    

    
}

