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
    var url = $(this).attr('data-value');
    var name = $(this).attr('data-name');
    //alert(val);
    $(this).parent().find('#choosen-category').val(url);
    $(this).parent().find('#choosen-category-name').val(name);
    });

    $('#show_answer').click(function(){
    var answer = $(this).attr('data-value');
    //alert(val);
    $('#answer').val(answer);
    });

    function copytext(el) {
    var $tmp = $("<textarea>");
    $("body").append($tmp);
    $tmp.val($(el).text()).select();
    document.execCommand("copy");
    $tmp.remove();
    };

    $('#copy-link').click(function(){
        copytext('#collapseUniqueUrl')
    });


});