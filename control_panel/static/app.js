$(function () {

    var main = $('.main');
    main.on('click', function (event){
        event.preventDefault();
        $(this).next().toggleClass('hidden');
    });

    var username = $('#username');
    username.on('click', function (event){
        event.preventDefault()
    });




});