jQuery(document).ready(function(){
    $('#count_now').click(function(){
        $.ajax({
            type: 'POST',
            url:'ajax.php',
            dataType: "json",
            data: {
                poem_body: $('#poem_body').val()
            }
        }).done(function( msg ) {
            console.log(msg)
            $('#Y1').val(msg.razmer + ' ' +msg.stop)
            $('#Y2').val(msg.lines_num)
            $('#Y3').val()
            $('#Y4').val(msg.m_end)
            $('#Y5').val(msg.g_end)
            $('#Y6').val(msg.d_end)
            $('#Y7').val()
            $('#Y8').val()
            $('#Y9').val()
            $('#Y10').val()
            $('#Y11').val()
        })
    })

})