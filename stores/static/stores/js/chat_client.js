(function (chatter, undefined) {

    chatter.decode_message = function (message_buffer, locale) {
        var dataview = new DataView(message_buffer);
        var decoder = new TextDecoder(locale || 'utf-8');
        return decoder.decode(dataview);
    };

    chatter.init = function () {
        var myself = this;
        var socket = io.connect('http://localhost:4000');
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
    };

    chatter.init();

}(window.chatter = window.chatter || {}));
