$(document).ready(function(){
    $("button[name='toggle']").html('<i class="fa fa-toggle-on"></i>');
    $("#myInput").on("keyup", function() {
        let value = $(this).val().toLowerCase();
    $("#session_table tr").filter(function() {
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

$('table').on('click-row.bs.table', function (row, element, field) {
    let id = element['id'];
    window.location = "/session_form/"+id;
});