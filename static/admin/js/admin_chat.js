(function (NS, $, _, io, ChatWidget, undefined) {
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
            ChatWidget.bindSocket(socket);
            socket.on('connect', function () {
                console.log('connect to agent');
            });
        }
    });
} (window.AdminChat = window.AdminChat || {}, $, _, io, window.ChatWidget));
