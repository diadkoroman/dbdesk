function Options(){
    var trm_ = $('#terminal_data')
    if(trm_.text()!=''){
        $('#term').show()
        }

    $('#options-menu a').click(function(){
        var id = $(this).attr('href')
        $(id).toggle()
        })
    }
$(document).ready(Options)
