(function (NS) {

    NS.SearchEntry = Backbone.Model.extend({
        idAttribute: 'key',
        _template: _.template('<option value="<%= key %>"><%= text %></option>'),
        get_html: function () {
            return this._template({
                key: this.get('key'),
                text: EDIK.capitalize(this.get('key'))
            });
        }
    });

    NS.SearchGroup = Backbone.Model.extend({
        idAttribute: 'key',
        _template: _.template('<optgroup label="<%= text %>"><%= entries %></optgroup>'),
        parse: function (response) {
            response.entries = new Backbone.Collection(_.map(response.entries, function (m) {
                return new NS.SearchEntry({
                    key: m,
                    group: response.key
                });
            }));
            return response;
        },
        get_html: function () {
            return this._template({
                text: EDIK.capitalize(this.get('key')),
                entries: this.get('entries').invoke('get_html').join('')
            });
        }
    });

    NS.SearchOptions = Backbone.Collection.extend({
        model: NS.SearchGroup,
        _template: _.template('<select class="search_options"><%= options %></select>'),
        parse: function (response) {
            var data = [];
            for (var group in response) {
                data.push({
                    key: group,
                    entries: response[group]
                });
            }
            return data;
        },
        get_html: function () {
            return this._template({
                options: this.invoke('get_html').join('')
            });
        }
    });

    _.extend(NS, {
        init: function (context) {
            this.search_options = new NS.SearchOptions(context, {parse: true});
            this.bind();
        },
        bind: function () {
            var $q = $('input[name="q"]');
            $q.on('change', _.bind(function () {
                var q = $q.val();
            }, this));
        },
        make_search_options: function () {
            var html = this.search_options.get_html();
            console.log(html);
        }
    });
})(window.StoreSearch = window.StoreSearch || {}, undefined);
