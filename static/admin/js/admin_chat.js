(function (NS, $, _, io, undefined) {
    _.extend(NS, {
        init: function (options) {
            this.options = options || {};
            this.bind();
        },
        bind: function () {
            this._bind_socket();
        },
        _bind_socket: function () {
            var socket = io.connect(this.options.socket_url);
            socket.on('connect', function () {
                console.log('connect to agent');
            });
            socket.on('message', function (resp) {
                console.log(resp);
            });
        }
    });
} (window.AdminChat = window.AdminChat || {}, $, _, io));
