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
            $('#Y3').val(msg.strofika)
            $('#Y4').val(msg.m_end)
            $('#Y5').val(msg.g_end)
            $('#Y6').val(msg.d_end)
            $('#Y7').val(msg.m_no)
            $('#Y8').val(msg.g_no)
            $('#Y9').val(msg.d_no)
            $('#Y10').val(msg.partial_line)
            $('#Y11').val(msg.strofika_type)

            $('.accent_wrap').html(msg.accent_log)
            $('.accent_sign').html(msg.accent_sign)
        })
    })

    $('#help_Y11').popover({html:true})
})