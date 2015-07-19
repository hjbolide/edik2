(function (NS, $, _, io, ChatWidget, undefined) {

    _.extend(NS, {
        init: function (options) {
            this.options = options || {};
            this.bind();
        },
        bind: function () {
            var myself = this;
            var socket = io.connect(this.options.socket_url);
            ChatWidget.bindSocket(socket);
            socket.on('connect', function () {
                console.log('connect to agent');
            });
        },
        decode_message: function (message_buffer, locale) {
            var dataview = new DataView(message_buffer);
            var decoder = new TextDecoder(locale || 'utf-8');
            return decoder.decode(dataview);
        }
    });

}(window.ChatClient = window.ChatClient || {}, $, _, io, window.ChatWidget));
