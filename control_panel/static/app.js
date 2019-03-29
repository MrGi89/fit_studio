$(function () {


    // Handles update member profile btn and ajax call
    const updBtn = $('#upd-btn');
    updBtn.hide();
    $('.profile-details').find('input, select, textarea').change(function () {
        updBtn.show()
    });
    $('#bday').find('input').datepicker({
        'dateFormat': 'yy-mm-dd',
        'showAnim': 'slideDown'});


});