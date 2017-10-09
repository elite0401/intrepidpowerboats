// eslint-disable-next-line
function createSlider(gallery) {
     return $(gallery).find('.bxslider').bxSlider({
         infiniteLoop: false,
         controls: true,
         pager: false
     });
 }
