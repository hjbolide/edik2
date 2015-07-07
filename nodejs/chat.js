(function () {
    var http = require('http');
    var server = http.createServer().listen(4000);
    var io = require('socket.io')(server);
    var cookie_reader = require('cookie'),
        querystring = require('querystring'),
        redis_adapter = require('socket.io-redis'),
        redis = require('redis').createClient;

    var sub = redis(6379, 'localhost', { detect_buffers: true });
    redis_adapter({ subClient: sub });
    sub.subscribe('stores_chat');

    io.use(function (socket, next) {
        var data = socket.request;
        if (data.headers.cookie) {
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return next(null, true);
        }
        return next('error', false);
    });

    io.on('connection', function (socket) {
        sub.on('message', function (channel, message) {
            socket.send(message);
        });

        socket.on('send_message', function (message) {
            var values = querystring.stringify({
                message: message,
                sessionid: socket.request.cookie['sessionid']
            });
            var options = {
                host: 'localhost',
                port: 8000,
                path: '/stores/chatter',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Content-Length': values.length
                }
            };

            var req = http.request(options, function (res) {
                res.setEncoding('utf8');
                var body = [];
                res.on('data', function (message) {
                    body.push(message);
                });
                res.on('end', function () {
                    console.log(body.join(''));
                });
            }).on('error', function (err) {
                console.log('---------');
                console.log(err);
            });

            req.write(values);
            req.end();
        });
    });
})();
