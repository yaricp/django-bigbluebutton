$(document).ready(function() {
    $('.more-info').click(function() { $(this).parent().find('.info').toggle() });
    $('.more-info').hover(
        function(){
            var pos=$(this).position();
            i=$(this).find('.info');
            i.css( 'left',pos.left+10);
            i.css('top', pos.top+10);
            i.fadeIn();
            },
        function(){
            $(this).find('.info').fadeOut()
        });
    
    });
