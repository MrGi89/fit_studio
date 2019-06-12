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
    $('#add-member-btn').click(addMember);
    $('#update-member-btn').click(updateMember);


    function updateMember() {

        const form = $('#update-member-form');
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'first_name': form.find("input[name='first_name']").val(),
            'last_name': form.find("input[name='last_name']").val(),
            'gender': form.find("select[name='gender'] option:selected").val(),
            'birth_date': form.find("input[name='birth_date']").val(),
            'status': form.find("select[name='status']  option:selected").val(),
            'mail': form.find("input[name='mail']").val(),
            'phone': form.find("input[name='phone']").val(),
            'notes': form.find("textarea[name='notes']").val(),
        };

        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/update/member/mem-pk/'.replace('mem-pk', form.attr('data-member-pk')),
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');

            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                $('.upd-btn').hide()
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
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

    function addMember() {

        const form = $('#add-member-form');
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'first_name': form.find("input[name='first_name']").val(),
            'last_name': form.find("input[name='last_name']").val(),
            'gender': form.find("select[name='gender'] option:selected").val(),
            'birth_date': form.find("input[name='birth_date']").val(),
            'status': form.find("select[name='status']  option:selected").val(),
            'mail': form.find("input[name='mail']").val(),
            'phone': form.find("input[name='phone']").val(),
            'notes': form.find("textarea[name='notes']").val(),
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