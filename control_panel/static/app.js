$(function () {


    // Handles update member profile btn
    $('.profile-details').find('input, select, textarea').change(function () {
        $('.upd-btn').show()
    });

    // Handles datepicker inputs
    $('.date-picker').find('input').datepicker({
        'dateFormat': 'yy-mm-dd',
        'showAnim': 'slideDown'
    });

    // changes price value in pass modal
    const passForm = $('#add-pass-form');
    const product = passForm.find("select[name='product']");
    const price = passForm.find("input[name='price']");
    product.change(function () {
        price.val(product.attr(`data-product-${product.find("option:selected").val()}`));
    });

    // Handles first-col slide
    // $(window).scroll(function () {
    //     $(".side-bar").stop().animate({
    //         "marginTop": ($(window).scrollTop()) + "px",
    //         "marginLeft": ($(window).scrollLeft()) + "px"
    //     }, "slow");
    // });

});
