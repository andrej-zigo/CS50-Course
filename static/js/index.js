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

    /* About - Tab Functionality */
    viewTab('skills', "skill-head")

});


/* About - Tab Function */
function viewTab(tabName, tabHead){
    $('.tab').removeClass('active');
    $('#' + tabHead).toggleClass('active');

    $('.tab').css({color: "var(--primary-text)"});
    $('#' + tabHead).css({color: "var(--red)"});

    $('.tab-contents').css({display: "none"});
    $('.' + tabName).css({display: "block"});
}
