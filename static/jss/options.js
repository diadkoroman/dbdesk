function Options(){
    var trm_ = $('#terminal_data')
    if(trm_.text()!=''){
        $('#term').show()
        }
    $('.query').click(function(){
        var q=$(this).attr('query')
        trm_.empty().html(q)
    })
}
$(document).ready(Options)
