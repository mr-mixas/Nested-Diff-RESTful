function diff() {
    hide_result_fields();

    try {
        var a = JSON.parse($('#dif-a').val());
        var b = JSON.parse($('#dif-b').val());
    } catch(err) {
        show_error(err);
        return;
    }

    $.ajax({
        type: 'POST',
        url: '/diff',
        contentType: 'application/json',
        data: JSON.stringify({
            a: a,
            b: b,
            diff_opts: {
                A: $('#dif-opt-A').is(':checked'),
                N: $('#dif-opt-N').is(':checked'),
                O: $('#dif-opt-O').is(':checked'),
                R: $('#dif-opt-R').is(':checked'),
                U: $('#dif-opt-U').is(':checked'),
                multiline_diff_context: Number($('#dif-opt-text-ctx').val()),
            },
            ofmt: $('#dif-ofmt').val(),
        })
    }).done(function(data, textStatus, xhr) {
        if ($('#dif-ofmt').val() == 'json') {
            show_diff_text(JSON.stringify(data, null, 2));
        } else if ($('#dif-ofmt').val() == 'term') {
            var ansi_up = new AnsiUp;
            var html = ansi_up.ansi_to_html(data);
            show_diff_html('<span>' + html + '</span>');
        } else if ($('#dif-ofmt').val() == 'html') {
            show_diff_html(data);
        } else {
            show_diff_text(data);
        }
    }).fail(function(data, textStatus) {
        show_error(data['statusText'] + ': ' + data['responseText']);
    })
}

function hide_result_fields() {
    $('.dif-result').each(function(){
        $(this).addClass('d-none');
    });
}

function show_diff() {
    $('#dif-label').removeClass("d-none");
    $('#dif-body').removeClass("d-none");
}

function show_diff_html(html) {
    $('#dif-body').html(html);
    show_diff();
}

function show_diff_text(text) {
    $('#dif-body').text(text);
    show_diff();
}

function show_error(error) {
    $('#dif-error').html(error);
    $('#dif-error').removeClass('d-none');
}
