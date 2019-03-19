$(function () {

    function UpdateMember(){
        $('#update-member').show();
    }


    const updMemBtn = $('#update-member');
    updMemBtn.hide();
    $('.profile-details').find('input, select, textarea').change(UpdateMember)

});