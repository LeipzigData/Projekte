angular
    .module("app.services")
    .factory("JsonData", function($resource, $cacheFactory) {
        const localCache = $cacheFactory('JsonData');

        // Angular resource to fetch files inside /data/
        const res = $resource("data/:fileName", {
            fileName: "@fileName"
        }, {
            query: {
                isArray: true,
                cache: localCache
            }
        });

        res.getData = function(cb) {
            const me = this;
            me.query({
                fileName: "data.json"
            }, data => {
                delete data.$promise;
                delete data.$resolved;
                cb(data);
            });
        };

        return res;
    })

    .factory("JsonConfig", function($resource, $cacheFactory) {
        const localCache = $cacheFactory('JsonConfig');

        // Angular resource to fetch files inside /data/
        const res = $resource("data/:fileName", {
            fileName: "@fileName"
        }, {
            query: {
                isArray: false,
                cache: localCache
            }
        });

        res.getConfig = function(cb) {
            const me = this;
            me.query({
                fileName: "config.json"
            }, data => {
                delete data.$promise;
                delete data.$resolved;
                cb(data);
            });
        };

        return res;
    });
