$(function () {


    // Handles update member profile btn
    const updBtn = $('.upd-btn');
    updBtn.hide();
    $('.profile-details').find('input, select, textarea').change(function () {
        updBtn.show()
    });

    // Handles datepicker
    $('#bday').find('input').datepicker({
        'dateFormat': 'yy-mm-dd',
        'showAnim': 'slideDown'
    });

    // shows success alert after member delete




});
