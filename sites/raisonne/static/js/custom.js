/**
 * Created by Oleksandr Gula.
 * User: Tayg
 * Date: 03.06.2011
 * Time: 14:10
 */

String.prototype.format = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};


/* DJANGO CSRF
----------------------------------------------------------*/

(function($){
    $('html').ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
})(jQuery);


/* COLORBOX
----------------------------------------------------------*/
/*
(function($){
    $("a.[rel='colorbox']").colorbox();
})(jQuery);
*/


/* AUCTION
----------------------------------------------------------*/

(function($){
    $.fn.extend({
        auction: function(url, error_message) {
            
            var make_bid = function(parent, url, worklot_pk, error_message) {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {worklot_pk: worklot_pk},
                    dataType: 'json',
                    success: function(data) {
                        $(parent).find('.message').html(data.message);
                        $(parent).find('.lot-next-price .price').html(data.next_price);
                        $(parent).find('.lot-bid-count .count').html(data.bid_count);
                    },
                    error: function(data) {
                        $(parent).find('.message').html(error_message);
                    }
                });
            };
            
            return this.each(function() {
                var parent = this;
                var worklot_pk =  $(this).find('.worklot-pk').val();
                $(this).find('.make-bid').click(function() {
                    make_bid(parent, url, worklot_pk, error_message)
                });
            });
        }
    });
})(jQuery);
