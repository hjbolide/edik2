(function (NS, $, _, ChatWidget, undefined) {

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

            var $chat_panel = $('div.chat');
            socket.on('message', function (resp) {
                $chat_panel.append('<p>' + myself.decode_message(resp) + '</p>');
                $chat_panel.focus();
            });

            var $chat_input = $('input[name="chat_input"]');
            $chat_input.on('change', function (e) {
                var msg = $chat_input.val();
                if (msg.trim()) {
                    socket.emit('send_message', msg, function (data) {
                        console.log(data);
                    });
                }
                $chat_input.val('');
            });
        },
        decode_message: function (message_buffer, locale) {
            var dataview = new DataView(message_buffer);
            var decoder = new TextDecoder(locale || 'utf-8');
            return decoder.decode(dataview);
        }
    });

}(window.ChatClient = window.ChatClient || {}, $, _, window.ChatWidget));
