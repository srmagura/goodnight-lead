//Used to create columns of equal height within bootstrap 3 rows,
//since there is no convenient native way to do so.



$(window).load(function() {
    if($size == "full") {
        $('.col-equal-height').children().height($('.col-equal-height').parent().height());
    }
});

$(window).resize(function() {
    //Only if the size changes to full
    if($size != $prev_size && $size == "full") {
        $('.col-equal-height').children().height($('.col-equal-height').parent().height());
    }
});
