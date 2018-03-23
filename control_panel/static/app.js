$(function () {

    var item = $('.dropdown_item');
    item.on('click', function (event){
        event.preventDefault();
        $(this).next().toggleClass('hidden');
    });


});