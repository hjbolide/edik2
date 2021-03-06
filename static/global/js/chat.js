(function (NS, $, _, io, EDIK, undefined) {
    _.extend(NS, {
        init: function (options) {
            this.options = options || {};
            this.bind();
        },
        bind: function () {
            this._bind_chat_widget();
        },
        _bind_chat_widget: function () {
            $(document).on('click', '.panel-heading span.icon_minim', function (e) {
                var $this = $(this);
                if (!$this.hasClass('panel-collapsed')) {
                    $this.parents('.panel').find('.panel-body').slideUp();
                    $this.addClass('panel-collapsed');
                    $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
                } else {
                    $this.parents('.panel').find('.panel-body').slideDown();
                    $this.removeClass('panel-collapsed');
                    $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
                }
            });
            $(document).on('focus', '.panel-footer input.chat_input', function (e) {
                var $this = $(this);
                if ($('#minim_chat_window').hasClass('panel-collapsed')) {
                    $this.parents('.panel').find('.panel-body').slideDown();
                    $('#minim_chat_window').removeClass('panel-collapsed');
                    $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
                }
            });
            $(document).on('click', '#new_chat', function (e) {
                var size = $( ".chat-window:last-child" ).css("margin-left");
                size_total = parseInt(size) + 400;
                alert(size_total);
                var clone = $( "#chat_window_1" ).clone().appendTo( ".container" );
                clone.css("margin-left", size_total);
            });
            $(document).on('click', '.icon_close', function (e) {
                //$(this).parent().parent().parent().parent().remove();
                $( "#chat_window_1" ).remove();
            });
        },
        _sent_template: _.template(
            '<div class="row msg_container base_sent">' +
                '<div class="col-md-10 col-xs-10"><div class="messages msg_sent">' +
                '<p><%= message_content %></p>' +
                '<time datetime="<%= message_timestamp %>"><%= message_timestamp_text %></time>' +
                '</div></div>' +
                '<div class="col-md-2 col-xs-2 avatar">' +
                '<img src="" class="img-responsive" /></div>'
        ),
        _receive_template: _.template(
            '<div class="row msg_container base_receive">' +
                '<div class="col-md-2 col-xs-2 avatar">' +
                '<img src="" class="responsive"/></div>' +
                '<div class="col-md-10 col-xs-10"><div class="messages msg_receive">' +
                '<p><%= message_content %></p>' +
                '<time datetime="<%= message_timestamp %>"><%= message_timestamp_text %></time>' +
                '</div></div></div>'
        ),
        add_chat_entry: function (chat_type, chat_data) {
            var template = chat_type === 'sent' ? this._sent_template : this._receive_template;
            $("div.msg_container_base").append(template(chat_data));
            // scroll
            // steal focus
            // alert
        },
        bindSocket: function (socket) {
            this.socket = socket;
            var $input = $('input[name="chat_message_input"]');
            $input.on('keyup', _.bind(function (e) {
                var code = e.keyCode || e.which;
                if (code === 13) {
                    var msg = $input.val();
                    var timestamp = new Date();
                    this._on_send(msg);
                    this.add_chat_entry('sent', {
                        message_content: msg,
                        message_timestamp: timestamp,
                        message_timestamp_text: EDIK.timestamp(timestamp)
                    });
                    $input.val('');
                }
            }, this));
            socket.on('message', _.bind(function (msg) {
                var timestamp = new Date();
                this.add_chat_entry('receive', {
                    message_content: msg,
                    message_timestamp: timestamp,
                    message_timestamp_text: EDIK.timestamp(timestamp)
                });
            }, this));
        },
        _on_send: function (msg) {
            this.socket.emit('send_message', msg, function (data) {
                console.log(data);
            });
        }
    });

    NS.init();

} (window.ChatWidget = window.ChatWidget || {}, $, _, io, window.EDIK));
