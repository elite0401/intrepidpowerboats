/*
 * Tooltip and Image preview script 
 * powered by jQuery (http://www.jquery.com)
 * 
 * written by Alen Grakalic (http://cssglobe.com)
 * 
 * for more info visit http://cssglobe.com/post/1620/image-preview
 *
 */

imagePreview = function(){
    /* CONFIG */

    xOffset = 10;
    yOffset = 30;

    // these 2 variable determine popup's distance from the cursor
    // you might want to adjust to get the right result

    /* END CONFIG */
    $("div.preview")
        .hover(function(e){
            var preview = "<div id='imagePreview'><p class='txt-green'>" + this.textContent + "</p>";
            if (this.dataset.thumbnail) {
                preview += "<img src='"+ this.dataset.thumbnail +"' />";
            }
            if (this.dataset.vimeo) {
                preview += "<iframe src='https://player.vimeo.com/video/"+ this.dataset.vimeo
                    + "?autoplay=1&title=0&byline=0&portrait=0' frameborder='0' width='180'></iframe>";
            }
            preview += "</div>";
            $("body").append(preview);

            $("#imagePreview")
                .css("top",(e.pageY - xOffset) + "px")
                .css("left",(e.pageX + yOffset) + "px")
                .fadeIn("fast");
            },
            function(){
                $("#imagePreview").remove();
            })
        .mousemove(function(e){
            $("#imagePreview")
                .css("top",(e.pageY - xOffset) + "px")
                .css("left",(e.pageX + yOffset) + "px");
        });
};

// starting the script on page load
$(document).ready(function(){
    imagePreview();
});
