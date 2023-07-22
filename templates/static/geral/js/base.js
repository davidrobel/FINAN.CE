function active() {
    $(document).on('click', 'a', function() {
        $(this).addClass('active')
    })    
}