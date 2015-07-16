(function (NS, $, _, undefined) {

    _.extend(NS, {
        init: function () {
            this.bind();
        },

        bind: function () {
            $('table.table').floatThead();
            $('input[data-edik-elem="roster-submit"]').on('click', _.bind(this.on_save, this));
            $('input[name="roster_day"]').on("change", _.bind(this.on_toggle_roster_day, this));
        },

        on_toggle_roster_day: function (e) {
            var $target = $(e.target);
            var $tr = $target.closest('tr[data-edik-elem^="roster_"]');
            var $roster = $tr.find('input[name=roster]');
            var roster = parseInt($roster.val(), 10),
                roster_mask = parseInt($target.val(), 10);
            if ($target.prop('checked')) {
                $roster.val(roster | roster_mask);
            } else {
                $roster.val(roster & (0b1111111 ^ roster_mask));
            }
        },

        collect_roster: function () {
            var roster_data = {};
            $('tr[data-edik-elem^="roster_"]').each(function (i, m) {
                var $row = $(m);
                roster_data[$row.find('input[name="person"]').val()] =
                    $row.find('input[name="roster"]').val();
            });
            return roster_data;
        },

        on_save: function () {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
                }
            });
            $.ajax({
                url: "/admin/stores/personadminviewmodel/save/",
                type: "POST",
                data: this.collect_roster(),
                success: function (response) {
                    var $alert_div = $('div.alert-div'),
                        msg = '';
                    if (response.success) {
                        $alert_div.removeClass(['alert-danger']).addClass('alert-success');
                        msg = "Successfully updated the roster.";
                    } else {
                        $alert_div.removeClass(['alert-success']).addClass('alert-danger');
                        msg = "Failed to update roster.";
                    }
                    $alert_div.find('span[data-edik-elem="alert-msg"]').text(msg);
                    $alert_div.fadeIn("fast").delay(2000).fadeOut("fast");
                },
                failure: function (error) {
                    console.log(error);
                }
            });
        }
    });

    NS.init();
    $('table.table').floatThead();
}(window.Roster = window.Roster || {}, $, _));
