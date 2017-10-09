$(function () {
    var interiorSlider = $('.interior-bxslider').bxSlider({
        pagerCustom: '#interior-pager',
        onSlideAfter: function () {
            this.redrawSlider();
        }
    });

    var exteriorSlider = $('.exterior-bxslider').bxSlider({
        pagerCustom: '#exterior-pager',
        onSlideAfter: function () {
            this.redrawSlider();
        }
    });
    
    var cabinSlider = $('.cabin-bxslider').bxSlider({
        pagerCustom: '#cabin-pager',
        onSlideAfter: function () {
            this.redrawSlider();
        }
    });

    var interiorGallery = $('.interior-gallery');
    var exteriorGallery = $('.exterior-gallery');
    var cabinGallery = $('.cabin-gallery');
    var interiorSelector = $('.interior-selector');
    var exteriorSelector = $('.exterior-selector');
    var cabinSelector = $('.cabin-selector');

    interiorSelector.click(function (event) {
        event.preventDefault();
        exteriorGallery.hide();
        cabinGallery.hide();
        interiorGallery.show();
        interiorSlider.reloadSlider();
        interiorSelector.addClass('on active').siblings().removeClass('on active');
        $('.carousel-inner').find('div').find('a').removeClass('selected');
    });

    exteriorSelector.click(function (event) {
        event.preventDefault();
        interiorGallery.hide();
        cabinGallery.hide();
        exteriorGallery.show();
        exteriorSlider.reloadSlider();
        exteriorSelector.addClass('on active').siblings().removeClass('on active');
        $('.carousel-inner').find('div').find('a').removeClass('selected');
    });

    cabinSelector.click(function (event) {
        event.preventDefault();
        interiorGallery.hide();
        exteriorGallery.hide();
        cabinGallery.show();
        cabinSlider.reloadSlider();
        cabinSelector.addClass('on active').siblings().removeClass('on active');
        $('.carousel-inner').find('div').find('a').removeClass('selected');
    });

    $('.carousel').carousel('pause');
    $('.dropdown-toggle').dropdown();

    $('.carousel-inner').find('div').find('a').on('click touchend', function () {
        $(this).addClass('selected').siblings().removeClass('selected');
    });
});

// Show slider when switching to About tab
$(".nav-tabs a[href='#about']").on('shown.bs.tab', function () {
    $('.exterior-bxslider').data('bxSlider').redrawSlider();
});
