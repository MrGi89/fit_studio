$(function () {


    // Handles update member profile btn
    $('.profile-details').find('input, select, textarea').change(function () {
        $('.upd-btn').show()
    });

    // Handles datepicker inputs
    $('#bday').find('input').datepicker({
        'dateFormat': 'yy-mm-dd',
        'showAnim': 'slideDown'
    });
    $('.date-picker').find('input').datepicker({
        'dateFormat': 'yy-mm-dd',
        'showAnim': 'slideDown'
    });

    // shows success alert after member delete




});
