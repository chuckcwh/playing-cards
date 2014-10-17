//{% load staticfiles %}
$(document).ready(function(){
var user_deck;
var dealer_deck;
var count = 0;

    $.ajax({
        url: '/war_all_draw/',
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            user_deck = data[0];
            dealer_deck = data[1];
        }
    });



    $('#draw').on('click', function(){
        user_get = user_deck[count];
        dealer_get = dealer_deck[count];
        count ++;
        user_get_image = user_get.split('"')[5];
        dealer_get_image = dealer_get.split('"')[5];
        console.log(user_get);
        console.log(user_get_image);
        var imgHtml = '<img width="100px" src="{% STATIC "' +  user_get_image + '%}" />';
        console.log(imgHtml);
        $('#player_card').html(imgHtml);
    });

});