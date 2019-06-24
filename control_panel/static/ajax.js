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

    $('#add-member-btn').click(addMember);
    $('#update-member-btn').click(updateMember);
    const successAlert = $("#success-alert");
    const failureAlert = $("#failure-alert");

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
            url: 'http://127.0.0.1:8000/update/member/mem-pk/'.replace('mem-pk', $('.profile').attr('data-member-pk')),
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                $('.upd-btn').hide();
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been correctly updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
                $.each(response, function (key, value) {
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
            failureAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Failure! </strong>There was a problem with your request! Please try again!');
            failureAlert.fadeTo(2000, 500).slideUp(500, function () {
                failureAlert.slideUp(500);
            });
        });
    }

    function addMember() {
        console.log('jestem');
        let result = false;
        const form = $('#add-member-form');
        console.log(form);
        const inputs = form.find('input, select, textarea');
        inputs.css('border-color', '#CED4DA');
        $('.invalid-input').hide();
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
            dataType: 'json',
            async: false
        }).done(function (response) {
            console.log(response);
            // validation passed
            if (response.result) {
                form.trigger('reset');
                result = true;
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been correctly updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
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
            result = true;
            failureAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Failure! </strong>There was a problem with your request! Please try again!');
            failureAlert.fadeTo(2000, 500).slideUp(500, function () {
                failureAlert.slideUp(500);
            });
        });
        return result;
    }


    // Handles add and update Product ajax call

    $('#add-product-btn').click(addProduct);
    const productUpdateBtn = $('.update-product-btn');
    productUpdateBtn.click(updateProduct);


    function updateProduct() {

        const product_pk = $(this).attr('data-product-pk');
        const form = $(`#update-product-form-${product_pk}`);
        const type = form.find("select[name='type'] option:selected");
        const activity = form.find("select[name='activity'] option:selected");
        const partner_name = form.find("select[name='partner_name'] option:selected");
        const validity = form.find("input[name='validity']");
        const available_entries = form.find("input[name='available_entries']");
        const price = form.find("input[name='price']");
        const deposit = form.find("input[name='deposit']");
        const entry_surcharge = form.find("input[name='entry_surcharge']");
        const absence_surcharge = form.find("input[name='absence_surcharge']");
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'type': type.val(),
            'activity': activity.val(),
            'partner_name': partner_name.val(),
            'validity': validity.val(),
            'available_entries': available_entries.val(),
            'price': price.val(),
            'deposit': deposit.val(),
            'entry_surcharge': entry_surcharge.val(),
            'absence_surcharge': absence_surcharge.val(),
        };

        $.ajax({
            type: 'POST',
            url: `http://127.0.0.1:8000/update/product/${product_pk}/`,
            data: formData,
            dataType: 'json',
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                const cols = $(`tr[data-product-pk='${product_pk}']`).children();
                cols.eq(1).text(type.val());
                cols.eq(2).text(available_entries.val());
                cols.eq(3).text(validity.val());
                cols.eq(4).text(price.val());
                cols.eq(5).text(deposit.val());
                cols.eq(6).text(entry_surcharge.val());
                cols.eq(7).text(absence_surcharge.val());
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Product has been correctly updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                inputs.css('border-color', '#00b000');
                delete response['result'];
                $.each(response, function (key, value) {
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
            failureAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Failure! </strong>There was a problem with your request! Please try again!');
            failureAlert.fadeTo(2000, 500).slideUp(500, function () {
                failureAlert.slideUp(500);
            });
        });
    }

    function addProduct() {
        console.log('jestem');
        let result = false;
        const form = $('#add-member-form');
        console.log(form);
        const inputs = form.find('input, select, textarea');
        inputs.css('border-color', '#CED4DA');
        $('.invalid-input').hide();
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
            dataType: 'json',
            async: false
        }).done(function (response) {
            console.log(response);
            // validation passed
            if (response.result) {
                form.trigger('reset');
                result = true;
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been correctly updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
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
            result = true;
            failureAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Failure! </strong>There was a problem with your request! Please try again!');
            failureAlert.fadeTo(2000, 500).slideUp(500, function () {
                failureAlert.slideUp(500);
            });
        });
        return result;
    }




});