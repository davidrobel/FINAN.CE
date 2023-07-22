$(document).on('click', 'a', function() {
    $(this).addClass('active').siblings().removeClass('active');
});