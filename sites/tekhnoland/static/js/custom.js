/**
 * Created by .
 * User: Tayg
 * Date: 14.03.11
 * Time: 14:10
 * To change this template use File | Settings | File Templates.
 */

String.prototype.format = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};


/* PAGE HEIGHT
----------------------------------------------------------*/

(function($) {
    function full_height(element, margins) {
        var target_height = element.parent().parent().height() - margins;
        var children_height = 0;
        element.children().each(function(index, child) {
            var child_height = $(child).height();
            if(children_height < child_height)
                children_height = child_height;
        });
        if(children_height < target_height)
            element.height(target_height);
    }
    $(function () {
        var element = $('#main-container');
        full_height(element, 290);
        $(window).resize(function() {
            full_height(element, 290);
        })
    });
})(jQuery);


/* HOVER
----------------------------------------------------------*/

(function($) {
    function define_hover(selector, class_normal, class_hover) {
        $(selector).hover(
            function () { $(this).removeClass(class_normal).addClass(class_hover); },
            function () { $(this).removeClass(class_hover).addClass(class_normal); }
       );
    }
    
    define_hover('#search-submit-container', 'sprites-button_find-png', 'sprites-button_find_hover-png');
    define_hover('#content-search-submit-container', 'sprites-button_find-png', 'sprites-button_find_hover-png');
    define_hover('#login-submit-container', 'sprites-button_login-png', 'sprites-button_login_hover-png');
    define_hover('#logout-submit-container', 'sprites-button_logout-png', 'sprites-button_logout_hover-png');
})(jQuery);


/* MENU
----------------------------------------------------------*/

(function($) {
    $('.menu-tree .menu-link').click(function() {
        if($(this).parent().children('.menu-tree').size() > 0) {
            $(this).parent().siblings().children('.menu-tree:visible').slideUp('slow');
            $(this).parent().children('.menu-tree').slideToggle('slow');
            return false;
        }
    });
    $('.menu-tree .menu-link').dblclick(function() {
        window.location = $(this).attr('href');
    });
    
    $('#menu-main .menu-item.active:not(:has(.menu-item.active))').addClass('active-selected');
})(jQuery);


/* FIX BROWSER UGLINESS
----------------------------------------------------------*/

(function($) {
    function fixChromeYellow() {
        $('.login-input').each(function() {
            t = $(this);
            t.clone().insertBefore(t);
            t.remove();
        });
    }
    $(function() {
        window.setTimeout(fixChromeYellow, 100);
    });
})(jQuery);


/* DJANGO CSRF
----------------------------------------------------------*/

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
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
});
