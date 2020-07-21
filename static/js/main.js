$(function(){
    var emojis = ["👶", "👦", "👨‍🎓", "🧙‍♂", '🤯'];

    $("input").mousemove(function () {
        var i = $(this).val();
        var j = parseInt(i, 10) + 1
        $(".emoji").html(emojis[i]);
        $(".level-number").html(j);
    });

    $('.category-group .category').click(function(){
    $(this).parent().find('.category').removeClass('selected');
    $(this).addClass('selected');
    var val = $(this).attr('data-value');
    //alert(val);
    $(this).parent().find('#choosen-category').val(val);
    });

});