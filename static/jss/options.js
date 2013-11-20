function Options(){
    var trm_ = $('#terminal_data')
    function check_terminal_data(){
        if(trm_.text()!=''){
            $('#term').show()
            }
    }

    $('#options-menu a').click(function(){
        check_terminal_data()
        var id = $(this).attr('href')
        var query = $(this).attr('query')
        trm_.empty().text(query)
        check_terminal_data()
        $(id).toggle()
        })
    }
$(document).ready(Options)
