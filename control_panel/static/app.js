$(function () {

    var item = $('.dropdown_item');
    item.on('click', function (event){
        event.preventDefault();
        $(this).next().toggleClass('hidden');
    });

    var passes = $('.passes');
        passes.on('click', function (event) {
            event.preventDefault();
            $(this).parent().parent().next().toggleClass('hidden')
        });

    var status = $('.status');
    status.each(function(index, element){
        if ($(this).text() === 'Opłacony'){
            $(this).parent().parent().addClass('success');
        }
    });

});