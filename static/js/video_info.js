function bind_submit_with_ajax()
{
    $("#video_info_download_form").submit(function( event ) {
        // cancels the form's submit action
        event.preventDefault();
    
        // informs the user the download will begin
        var new_elem = [
            '<div id="prepare_download_redirect" class="alert alert-info">',
            '<i class="fa fa-2x fa-spinner fa-spin"></i>',
            '<button type="button" class="close" data-dismiss="alert">×</button>',
            'Your download will begin shortly.',
            '</div>'].join('\n');
        $(".messages").append(new_elem);
        $('button[type="submit"]').attr('disabled', 'disabled');
    
        // handles the post and progress with jQuery
        var form = $(this);
        jQuery.ajax({
            url: form.attr("action"),
            method: 'POST',
            data: form.serialize()
        }).done(function (response) {
            // Do something with the response
            // alert("Done");
            // download ready, removes prepare download message and re-enables the download button
            $( "#prepare_download_redirect" ).remove();
            $('button[type="submit"]').removeAttr('disabled');
            // also adds the download link for the user to click if the javascript redirect doesn't work
            var download_redirect_url = response.download_redirect_url;
            var new_elem = [
                '<div class="alert alert-success">',
                '<i class="fa fa-2x fa-download"></i>',
                '<button type="button" class="close" data-dismiss="alert">×</button>',
                '<a href="' + download_redirect_url + '">',
                'Your download is ready, click here to download on your computer.</a>',
                '</div>'].join('\n');
            $(".messages").append(new_elem);
            // finally redirects to the file download
            window.location.replace(download_redirect_url);
        }).fail(function () {
            // Whoops; show an error.
            alert("Error");
        }).always(function () {
            $('button[type="submit"]').removeAttr('disabled');
        });
    });
}

// http://stackoverflow.com/questions/13437446/how-to-display-selected-item-in-bootstrap-button-dropdown-title
function improve_button_dropdown()
{
    $(".dropdown-menu li a").click(function(){
        $(".btn:first-child").html($(this).html());
        // $(".btn:first-child").val($(this).text());
    });
}
