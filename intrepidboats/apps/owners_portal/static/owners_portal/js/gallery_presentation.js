// eslint-disable-next-line
function createSlider(gallery) {
     return $(gallery).find('.bxslider').bxSlider({
         infiniteLoop: false,
         touchEnabled: false,
         video: true,
         pagerCustom: gallery + ' #bx-pager',
         nextSelector: gallery + ' #slider-next',
         nextText: '&gt;|'
     });
 }
