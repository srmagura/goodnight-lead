//Used to create columns of equal height within bootstrap 3 rows,
//since there is no convenient native way to do so.



$(window).load(function() {
    if($size == "full") {
        $('.col-equal-height').children().height($('.col-equal-height').parent().height());
    }
});

//Override the default resize
sizeChange = function() {
    if($size == "full") {
        $('.col-equal-height').children().height($('.col-equal-height').parent().height());
    }
    else {
        $('.col-equal-height').children().height('auto');
    }
}
