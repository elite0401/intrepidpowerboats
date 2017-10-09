$(function () {
    var search = location.search;
    if (search) {
        if (search.indexOf("page") >= 0) {
            var amountOfPreviousPages = parseInt(search.split("page=")[1]) - 1;
            var articleItemHeight = $('.article-item').height();
            // * 3 (paginated_by = 3)
            // * amountOfPreviousPages (by the amount of "pages" that there are before)
            // + 500 (header height)
            var yScroll = articleItemHeight * 3 * amountOfPreviousPages + 550;
            window.scrollTo(0, yScroll);
        }
    }
});