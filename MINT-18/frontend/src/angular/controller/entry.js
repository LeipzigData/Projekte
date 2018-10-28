angular
    .module("app")
    .controller("EntryController",
        function($scope,
            $routeParams,
            JsonData,
            JsonConfig,
            $anchorScroll,
            $timeout) {

            let loadMap = () => {
                if (!$scope.validMap) {
                    return;
                }
                // Only create the map if it does not exist already
                if ($scope.map) {
                    return;
                }
                // LatLong position of the entry
                let entryPosition = [
                    $scope.entry.gps.lat,
                    $scope.entry.gps.long
                ];
                $scope.map = L.map('map').setView(entryPosition, 13);
                // Setup map
                L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    maxZoom: 18,
                    id: 'mapbox.streets',
                    accessToken: 'pk.eyJ1IjoibWVnYW1hbm1hbHRlIiwiYSI6ImNqbDR5bG1rOTFpc2wzdnF5eTJ0dnhtemsifQ.RCMTLOjQri0YrwcqeDXqeA'
                }).addTo($scope.map);
                // Add the marker to the map
                let marker = L.marker(entryPosition);
                // Add a nice uncloseable popup
                marker.bindPopup(`<b>${$scope.entry.name}</b>`, {
                    closeButton: false,
                    autoClose: false,
                    closeOnEscapeKey: false,
                    closeOnClick: false
                });
                marker.addTo($scope.map);
                // Bad way of handling container size changes due to ng-show
                // TODO Improve
                setTimeout(() => {
                    $scope.map.invalidateSize();
                    marker.openPopup();
                }, 100);
            };

            let tags = [];
            $scope.iconFromTag = tagName => {
                let matching = tags.filter(tag => tag.name == tagName);
                if (matching.length > 0) {
                    return matching[0].icon;
                }
                return "fa-question";
            };

            // Accessibility to traffic light color
            $scope.accessibilityToColor = accessibility => {
                if (accessibility === 1) {
                    return 'orange';
                } else if (accessibility === 2) {
                    return 'green';
                }
                return 'red';
            };

            // Accessibility to description
            $scope.accessibilityToText = accessibility => {
                if (accessibility === 1) {
                    return 'Eingeschränkt Barrierefrei';
                } else if (accessibility === 2) {
                    return 'Barrierefrei';
                } else {
                    return 'Nicht Barrierefrei';
                }
            };

            // Fetch the data and filter for the currently viewed entry
            JsonData.getData(function(data) {
                $scope.data = data;
                $scope.data
                    .filter(el => el.id.toString() === $routeParams.entryId)
                    .forEach(el => {
                        // Expose extend object
                        el = Object.assign(el, el.extend);
                        delete el.extend;
                        $scope.entry = el;
                    });

                // Are we able to display a map correctly?
                $scope.validMap =
                    $scope.entry.gps != null &&
                    $scope.entry.gps.lat != null &&
                    $scope.entry.gps.long != null;
                loadMap();
            });

            // Fetch the configuration for the tag icons
            JsonConfig.getConfig(config => {
                tags = config.tags;
            });

            $anchorScroll();
        });
