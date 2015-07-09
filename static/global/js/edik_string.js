(function (NS) {
    _.extend(NS, {
        capitalize: function (string) {
            return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase();
        }
    });
})(EDIK = window.EDIK || {}, undefined);
