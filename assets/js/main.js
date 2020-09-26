$( document ).ready(function() {

    $( "a[id^='openPublishBtn']" ).each(function( index ) {
        var url = $(this).data('action');
        $(this).click( function() {
            $('#publishDraft').attr('action', '');
            $('#publishDraft').attr('action', url);
        });  
    });

    $( "a[id^='openArchiveBtn']" ).each(function( index ) {
        var url = $(this).data('action');
        $(this).click( function() {
            $('#archiveDraft').attr('action', '');
            $('#archiveDraft').attr('action', url);
        });  
    });


    $( "a[id^='openDeleteBtn']" ).each(function( index ) {
        var url = $(this).data('action');
        $(this).click( function() {
            $('#deleteDraft').attr('action', '');
            $('#deleteDraft').attr('action', url);
        });  
    });

})






