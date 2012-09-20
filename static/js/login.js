$(function() {
    var $form_inputs = $('form input');
    var $rainbow_and_border = $('.rain, .border');
    /* Used to provide loping animations in fallback mode */
    $form_inputs.bind('focus', function() {
        $rainbow_and_border.addClass('end').removeClass('unfocus start');
    });
    $form_inputs.bind('blur', function() {
        $rainbow_and_border.addClass('unfocus start').removeClass('end');
    });
    $form_inputs.first().delay(800).queue(function() {
        $(this).focus();
    });
});

