//$(function() {
//    $('#markup_bt').css("background-color", "#7ecbc6");
//})

//$(function() {
//    $('.descriptor').click(function (){
//        alert('its working!');
//    });
//})



$(function() {
    $('#markup_bt').on('click', function() {
        $(".try").removeAttr("hidden");
        //alert('its working!');
    });
})
