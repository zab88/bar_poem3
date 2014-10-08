jQuery(document).ready(function(){
    $('#count_now').click(function(){
        $.ajax({
            type: 'POST',
            url:'ajax.php',
            data: {
                poem_body: $('#poem_body').val()
            }
        }).done(function( msg ) {
            console.log(msg)
        })
    })

})