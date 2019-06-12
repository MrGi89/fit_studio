$(function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // Handles update Member ajax call from main modal

    $('.mem-success').hide();
    $('.add-member-btn').click(addMember);


    function addMember() {

        const form = $('#add-member-form');
        const first_name = form.find("input[name='first_name']");
        const last_name = form.find("input[name='last_name']");
        const gender = form.find("select[name='gender'] option:selected");
        const birth_date = form.find("input[name='birth_date']");
        const status = form.find("select[name='status']  option:selected");
        const mail = form.find("input[name='mail']");
        const phone = form.find("input[name='phone']");
        const notes = form.find("textarea[name='notes']");
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'first_name': first_name.val(),
            'last_name': last_name.val(),
            'gender': gender.val(),
            'birth_date': birth_date.val(),
            'status': status.val(),
            'mail': mail.val(),
            'phone': phone.val(),
            'notes': notes.val(),
        };

        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/create/member/',
            data: formData,
            dataType: 'json'
        }).done(function (response) {

            if (response.result) {
                form.hide();
                $('.mem-next').hide();
                $('.mem-success').show()
            } else {

                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function(key, value) {
                    const input = form.find("[name='input']".replace('input', key));
                    if ($.inArray(input.attr('name'), ['gender', 'status']) === 0) {
                        input.parent().next().text(value);
                        input.parent().css('border-color', '#FF0000');
                        input.parent().next().show();
                    } else {
                        input.next().text(value);
                        input.css('border-color', '#FF0000');
                        input.next().show();
                    }
                });
            }
        }).fail(function () {
            alert('Sorry, there was a problem! Please try again!')
        });
    }
});