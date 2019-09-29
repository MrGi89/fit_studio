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

    const successAlert = $("#success-alert");
    const failureAlert = $("#failure-alert");
    const warningAlert = $("#warning-alert");

    $('#add-member-btn').click(addMember);
    function addMember() {

        let result = false;
        const form = $('#add-member-form');
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
            url: '/create/member/',
            data: formData,
            dataType: 'json',
            async: false
        }).done(function (response) {
            // validation passed
            if (response.result) {
                form.trigger('reset');
                result = true;
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been successfully added');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
                if ($('#category').text() === 'MEMBERS') {
                    warningAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Warning! </strong>Refresh page to view added member');
                    warningAlert.fadeTo(2000, 500)
                }


                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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
            url: `/update/member/${$(this).attr('data-pk')}/`,
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                $('.upd-btn').hide();
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been successfully updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    // TRAINER CREATE AND UPDATE

    $('#add-trainer-btn').click(addTrainer);
    function addTrainer() {

        let result = false;
        const form = $('#add-trainer-form');
        const inputs = form.find('input, select, textarea');
        inputs.css('border-color', '#CED4DA');
        $('.invalid-input').hide();
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'first_name': form.find("input[name='first_name']").val(),
            'last_name': form.find("input[name='last_name']").val(),
            'gender': form.find("select[name='gender'] option:selected").val(),
            'birth_date': form.find("input[name='birth_date']").val(),
            'status': form.find("select[name='status'] option:selected").val(),
            'mail': form.find("input[name='mail']").val(),
            'phone': form.find("input[name='phone']").val(),
            'hourly_rate': form.find("input[name='hourly_rate']").val(),
            'employment_type': form.find("select[name='employment_type'] option:selected").val(),
            'notes': form.find("textarea[name='notes']").val(),
        };
        $.ajax({
            type: 'POST',
            url: '/create/trainer/',
            data: formData,
            dataType: 'json',
            async: false
        }).done(function (response) {
            // validation passed
            if (response.result) {
                form.trigger('reset');
                result = true;
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Trainer has been successfully added');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
                if ($('#category').text() === 'TRAINERS') {
                    warningAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Warning! </strong>Refresh page to view added trainer');
                    warningAlert.fadeTo(2000, 500)
                }
                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    $('#update-trainer-btn').click(updateTrainer);
    function updateTrainer() {

        const form = $('#update-trainer-form');
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'first_name': form.find("input[name='first_name']").val(),
            'last_name': form.find("input[name='last_name']").val(),
            'gender': form.find("select[name='gender'] option:selected").val(),
            'birth_date': form.find("input[name='birth_date']").val(),
            'status': form.find("select[name='status']  option:selected").val(),
            'mail': form.find("input[name='mail']").val(),
            'phone': form.find("input[name='phone']").val(),
            'hourly_rate': form.find("input[name='hourly_rate']").val(),
            'employment_type': form.find("select[name='employment_type'] option:selected").val(),
            'notes': form.find("textarea[name='notes']").val(),
        };

        $.ajax({
            type: 'POST',
            url: `/update/trainer/${$(this).attr('data-pk')}/`,
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                $('.upd-btn').hide();
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been successfully updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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


// GROUP CREATE AND UPDATE

    $('#add-group-btn').click(addGroup);
    function addGroup() {

        let result = false;
        const form = $('#add-group-form');
        const inputs = form.find('input, select, textarea');
        inputs.css('border-color', '#CED4DA');
        $('.invalid-input').hide();
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'activity': form.find("select[name='activity'] option:selected").val(),
            'trainer': form.find("select[name='trainer'] option:selected").val(),
            'max_capacity': form.find("input[name='max_capacity']").val(),
            'level': form.find("select[name='level'] option:selected").val(),
            'color': form.find("input[name='color']").val(),
            'class_time': form.find("input[name='class_time']").val(),
            'days': form.find("select[name='days'] option:selected").val(),
        };
        $.ajax({
            type: 'POST',
            url: '/create/group/',
            data: formData,
            dataType: 'json',
            async: false
        }).done(function (response) {
            // validation passed
            if (response.result) {
                form.trigger('reset');
                result = true;
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Group has been successfully added');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
                if ($('#category').text() === 'GROUPS') {
                    warningAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Warning! </strong>Refresh page to view added group');
                    warningAlert.fadeTo(2000, 500)
                }
                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    $('#update-group-btn').click(updateGroup);
    function updateGroup() {

        const form = $('#update-group-form');
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'activity': form.find("select[name='activity'] option:selected").val(),
            'trainer': form.find("select[name='trainer'] option:selected").val(),
            'max_capacity': form.find("input[name='max_capacity']").val(),
            'level': form.find("select[name='level'] option:selected").val(),
            'color': form.find("input[name='color']").val(),
            'class_time': form.find("input[name='class_time']").val(),
            'days': form.find("select[name='days'] option:selected").val(),
        };

        $.ajax({
            type: 'POST',
            url: `/update/group/${$(this).attr('data-pk')}/`,
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                $('.upd-btn').hide();
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Group has been successfully updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

// PRODUCT CREATE AND UPDATE

    $('#add-product-btn').click(addProduct);
    function addProduct() {

        let result = false;
        const form = $('#add-product-form');
        const inputs = form.find('input, select, textarea');
        inputs.css('border-color', '#CED4DA');
        $('.invalid-input').hide();
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'type': form.find("select[name='type'] option:selected").val(),
            'activity': form.find("select[name='activity'] option:selected").val(),
            'partner_name': form.find("select[name='partner_name'] option:selected").val(),
            'validity': form.find("input[name='validity']").val(),
            'available_entries': form.find("input[name='available_entries']").val(),
            'price': form.find("input[name='price']").val(),
            'deposit': form.find("input[name='deposit']").val(),
            'entry_surcharge': form.find("input[name='entry_surcharge']").val(),
            'absence_surcharge': form.find("input[name='absence_surcharge']").val(),
        };
        $.ajax({
            type: 'POST',
            url: '/create/product/',
            data: formData,
            dataType: 'json',
            async: false
        }).done(function (response) {
            // validation passed
            if (response.result) {
                form.trigger('reset');
                result = true;
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Product has been successfully added');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
                if ($('#category').text() === 'PRODUCTS') {
                    warningAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Warning! </strong>Refresh page to view added product');
                    warningAlert.fadeTo(2000, 500)
                }
                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    // Handles update Product ajax call

    const productUpdateBtn = $('.update-product-btn');
    productUpdateBtn.click(updateProduct);

    function updateProduct() {

        const product_pk = $(this).attr('data-product-pk');
        const form = $(`#update-product-form-${product_pk}`);
        const type = form.find("select[name='type'] option:selected");
        const activity = form.find("select[name='activity'] option:selected");
        let partner_name = form.find("select[name='partner_name'] option:selected");
        const validity = form.find("input[name='validity']");
        let available_entries = form.find("input[name='available_entries']");
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
            url: `/update/product/${product_pk}/`,
            data: formData,
            dataType: 'json',
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                const cols = $(`tr[data-product-pk='${product_pk}']`).children();
                partner_name = partner_name.text() === '---------' ? '' : partner_name.text();
                available_entries = available_entries.val() ? available_entries.val() : '&infin;';
                cols.eq(1).text(`${type.text()} ${partner_name} ${activity.text()}`);
                cols.eq(2).html(available_entries);
                cols.eq(3).text(validity.val());
                cols.eq(4).text(price.val());
                cols.eq(5).text(deposit.val());
                cols.eq(6).text(entry_surcharge.val());
                cols.eq(7).text(absence_surcharge.val());
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Product has been successfully updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                inputs.css('border-color', '#00b000');
                delete response['result'];
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    // Handles add Pass ajax call

    $('#add-pass-btn').click(addPass);

    function addPass() {
        let result = false;
        const form = $('#add-pass-form');
        const inputs = form.find('input, select');
        inputs.css('border-color', '#CED4DA');
        $('.invalid-input').hide();

        const product = form.find("select[name='product'] option:selected");
        const start_date = form.find("input[name='start_date']");
        const end_date = form.find("input[name='end_date']");
        const paid = form.find("input[name='paid']");
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'product': product.val(),
            'start_date': start_date.val(),
            'end_date': end_date.val(),
            'paid': paid.is(':checked'),
            'member': $('.profile').attr('data-member-pk')
        };
        $.ajax({
            type: 'POST',
            url: '/create/pass/',
            data: formData,
            dataType: 'json',
            async: false
        }).done(function (response) {
            // validation passed
            if (response.result) {
                result = true;

                // const tableBody = $('#pass-table').find('tbody');
                // const paidTxt = paid.is(':checked') ? 'Opłacony': 'Nieopłacony';
                // if (tableBody.children().eq(0).children().eq(0).text() === 'No passes bought') {
                //     tableBody.children().eq(0).remove()
                // }
                // tableBody.prepend(`<tr>
                //                       <th scope="row">new</th>
                //                       <td>${product.text()}</td>
                //                       <td>${start_date.val()}</td>
                //                       <td>${end_date.val()}</td>
                //                       <td>0</td>
                //                       <td>${paidTxt}</td>
                //                       <td><a href="#"><i class="fa fa-info-circle"></i></a></td>
                //                       <td><a href="#"><i class="fas fa-trash-alt"></i></a></td>
                //                   </tr>`);
                // form.trigger('reset');
                // successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Member has been correctly added');
                // successAlert.fadeTo(2000, 500).slideUp(500, function () {
                //     successAlert.slideUp(500);
                // });

                // validation not passed
            } else {
                delete response['result'];
                form.find('input, select, textarea').css('border-color', '#00b000');
                $('.invalid-input').hide();
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    // Update user ajax call

    $('#update-user-btn').click(updateUser);

    function updateUser() {

        const form = $('#profile-form');
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'first_name': form.find("input[name='first_name']").val(),
            'last_name': form.find("input[name='last_name']").val(),
            'email': form.find("input[name='email']").val(),
            'password': form.find("input[name='password']").val(),
            'password_confirmation': form.find("input[name='password_confirmation']").val(),
        };

        $.ajax({
            type: 'POST',
            url: `/update/user/${form.attr('data-user-pk')}/`,
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>User has been successfully updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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

    // Update Studio ajax call

$('#update-studio-btn').click(updateStudio);

    function updateStudio() {

        const form = $('#studio-form');
        const formData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'name': form.find("input[name='name']").val(),
            'company_name': form.find("input[name='company_name']").val(),
            'street': form.find("input[name='street']").val(),
            'postal_code': form.find("input[name='postal_code']").val(),
            'city': form.find("input[name='city']").val(),
            'nip': form.find("input[name='nip']").val(),
            'regon': form.find("input[name='regon']").val(),
            'mail': form.find("input[name='mail']").val(),
            'phone': form.find("input[name='phone']").val()
        };

        $.ajax({
            type: 'POST',
            url: `/update/studio/1/`,
            data: formData,
            dataType: 'json'
        }).done(function (response) {
            $('.invalid-input').hide();
            const inputs = form.find('input, select, textarea');
            if (response.result) {
                inputs.css('border-color', '#CED4DA');
                successAlert.html('<button type="button" class="close" data-dismiss="alert">x</button><strong>Success! </strong>Studio has been successfully updated');
                successAlert.fadeTo(2000, 500).slideUp(500, function () {
                    successAlert.slideUp(500);
                });
            } else {
                delete response['result'];
                inputs.css('border-color', '#00b000');
                $.each(response, function (key, value) {
                    const input = form.find(`[name='${key}']`);
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






















});