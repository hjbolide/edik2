(function (NS) {

    NS.SearchEntry = Backbone.Model.extend({
        parse: function (data) {
            
        }
    });

    NS.SearchGroup = Backbone.Collection.extend({
        model: NS.SearchEntry
    });

    _.extend(NS, {
        init: function (context) {
            this.context = context;
        }
        ,bind: function () {
            var $q = $('input[name="q"]');
            $q.on('change', _.bind(function () {
                var q = $q.val();
                
            }, this));
        }
        ,make_search_options: function () {
        }
    });
})(window.StoreSearch = window.StoreSearch || {}, undefined);
