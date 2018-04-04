$(function () {

    var item = $('.dropdown_item');
    item.on('click', function (event){
        event.preventDefault();
        $(this).next().toggleClass('hidden');
    });

// Member-site: Shows and hides dates of entries

    var passes = $('.passes');
        passes.on('click', function (event) {
            event.preventDefault();
            $(this).parent().parent().next().toggleClass('hidden')
        });


// Member-site: Adds green color when pass has been paid

    var status = $('.status');
    status.each(function(index, element){
        if ($(this).text() === 'Opłacony'){
            $(this).parent().parent().addClass('success');
        }
    });

// Finances-site: Adds green color when pass has been paid

    var payments = $('.payment');
    payments.each(function(index, element){
        if ($(this).text() === 'Opłacony'){
            $(this).parent().addClass('success');
        } else {
            $(this).parent().addClass('danger');
        }
        });



// Group-site2:

    var option = $('#option');
    option.on('click', function (event) {
        event.preventDefault();
        option.siblings().toggleClass('hidden');

        
    })


});