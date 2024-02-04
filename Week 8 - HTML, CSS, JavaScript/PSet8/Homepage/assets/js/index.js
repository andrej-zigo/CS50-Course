$(document).ready(() => {


    /* Hamburger Functionality */
    $('.ham').click(function clickMenu() {
        $('.nav-elements').toggleClass('nav-visible');

        if ($('.nav-elements').hasClass('nav-visible')) {
            $('body').css("overflow", "hidden");
            $('.nav-link').click(() => {
                $('.ham').click();
                $('.ham').removesClass('active');
            })
            $('.nav-btn').click(() => {
                $('.ham').click();
                $('.ham').removesClass('active');
            })
        }
        else {
            $('body').css("overflow", "visible");
        }
    });
});
