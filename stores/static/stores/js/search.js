(function (NS, undefined) {
    _.extend(NS, {
        init: function (context) {
            this.search_options = new NS.SearchOptions(context, {parse: true});
            this.bind();
        },
        bind: function () {
            $('select.search_options').select2({hint: true});
        },
        make_search_options: function (keyword) {
            var html = this.search_options.get_html(keyword);
            $('div#select2-container').html(html);
            $('div.search_options').select2();
        }
    });
}(window.StoreSearch = window.StoreSearch || {}));
