$(document).ready(function(){
    $("button[name='toggle']").html('<i class="fa fa-toggle-on"></i>');
    $('table tr > *:nth-child(1)').hide();
    $("#myInput").on("keyup", function() {
        let value = $(this).val().toLowerCase();
    $("#catalog_table tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$.fn.stars = function() {
    return $(this).each(function() {
        let rating = $(this).data("rating");
        let numStars = $(this).data("numStars");
        let fullStar = new Array(Math.floor(rating + 1)).join('<i class="fa fa-star"></i>');
        let halfStar = ((rating%1) !== 0) ? '<i class="fa fa-star-half-empty"></i>': '';
        let noStar = new Array(Math.floor(numStars + 1 - rating)).join('<i class="fa fa-star-o"></i>');
        $(this).html(fullStar + halfStar + noStar);
    });
};
$('.stars').stars();



$.fn.difficulty_tag = function() {
    return $(this).each(function() {
        let diff = $(this).data("difficulty");
        if (diff <= 2) {
            $(this).attr("style", "background-color: #cb4b16;");
        } else if (diff <= 4){
            $(this).attr("style", "background-color: #839496;");
        } else if (diff <= 6) {
            $(this).attr("style", "background-color: #b58900;");
        } else if (diff <= 8) {
            $(this).attr("style", "background-color: #eee8d5;");
        } else if (diff <= 10) {
            $(this).attr("style", "background-color: #268bd2;");
        }

    });
};

$('#kbd_difficulty').difficulty_tag();

$('table').on('click-row.bs.table', function (row, element, field) {
    let id = element['id'];
    window.location = "/catalog/id/"+id;
});
