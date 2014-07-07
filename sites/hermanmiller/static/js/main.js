$(document).ready(function () {
    $('a.colorbox').colorbox({
        rel: 'content'
    });

    /* tabs */
    $('.js-tabs').tabs({ heightStyle: "auto" });
    $('.goods-small-img').tabs();

    /* slideshow */

    if ($('.slideshow').length) {
        $('.slideshow').cycle({
            fx: 'scrollHorz',
            prev: '.slideshow__btn-prev',
            next: '.slideshow__btn-next',
            pager: '.slideshow__pager',
            timeout: 5000
        });

        if ($('.slideshow__pager a').text() != '') {
            $('.slideshow__btn-prev, .slideshow__btn-next').show();
        }
    }

    $('.js-product-number').spinner({
        min: 0
    });

    $('.js-product-buy').button({
        icons: {
            primary: "ui-icon-cart"
        }
    });

    $('.js-cart-login').button({
        icons: {
            primary: "ui-icon-unlocked"
        }
    });

    $('.js-cart-logout').button({
        icons: {
            primary: "ui-icon-locked"
        }
    });

    $('.js-cart-continue').button({
        icons: {
            primary: "ui-icon-refresh"
        }
    });

    $('.js-cart-order').button({
        icons: {
            primary: "ui-icon-cart"
        }
    });

    /* nav */
    /* uncomment to make menu dinamic
     $('.nav__item').mouseover(function() {
     var dropWidth = 0,
     dropItem  = $(this).find('.nav__drop-item'),
     drop      = $(this).find('.nav__drop-frame');
     dropItem.each(function() {
     var itemWidth = $(this).innerWidth();
     dropWidth += itemWidth;
     });
     drop.css('width', dropWidth);
     });*/
});


/* Utils
 ----------------------------------------------------------*/
function calcSum(array, item_selector) {
    var total = 0;
    for (var i = 0; i < array.length; i++)
        total += item_selector(array[i]);
    return total;
}

function find(array, predicate) {
    for (var i = 0; i < array.length; i++) {
        if (predicate(array[i])) {
            return array[i];
        }
    }
    return undefined;
}


/* Knockout
 ----------------------------------------------------------*/

ko.bindingHandlers.spinner = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        var options = allBindingsAccessor().spinnerOptions || {};
        $(element).spinner(options);

        //handle the field changing
        ko.utils.registerEventHandler(element, "spinchange", function () {
            var observable = valueAccessor();
            observable($(element).spinner("value"));
        });

        //handle disposal (if KO removes by the template binding)
        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            $(element).spinner("destroy");
        });
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor()),
            current = $(element).spinner("value");

        if (value !== current) {
            $(element).spinner("value", value);
        }
    }
};

ko.bindingHandlers.slideVisible = {
    init: function (element, valueAccessor) {
        // Initially set the element to be instantly visible/hidden depending on the value
        var value = valueAccessor();
        $(element).toggle(ko.unwrap(value)); // Use "unwrapObservable" so we can handle values that may or may not be observable
    },
    update: function (element, valueAccessor) {
        var value = valueAccessor();
        ko.unwrap(value) ? $(element).slideDown() : $(element).slideUp();
    }
};

ko.extenders.validate = function (target, options) {
    //add some sub-observables to our observable
    target.isValid = ko.observable();
    target.validationMessage = ko.observable();

    //define a function to do validation
    function validate(newValue) {
        var valid = options.validator(newValue);
        target.isValid(valid);
        target.validationMessage(valid ? "" : options.message || "*");
    }

    //initial validation
    validate(target());

    //validate whenever the value changes
    target.subscribe(validate);

    //return the original observable
    return target;
};

function required(value) {
    return value ? true : false;
}

function requiredValidator(message) {
    return {
        validator: required,
        message: message
    };
}

function CartItem(parent, product) {
    var self = this;

    self.id = product.id;
    self.url = product.url;
    self.name = product.name;
    self.price_eur = product.price_eur;
    self.price_uah = product.price_uah;
    self.quantity = ko.observable(product.quantity);
}

function CartOrder(parent, order) {
    var self = this;

    self.name = ko.observable("").extend({validate: requiredValidator()});
    self.phone = ko.observable("").extend({validate: requiredValidator()});
    self.email = ko.observable("");
    self.code = ko.observable("");
    self.contact = ko.observable("");
    self.address = ko.observable("");
    self.payment_type = ko.observable("");
    self.comment = ko.observable("");

    self.isValid = ko.computed(function () {
        return self.name.isValid() && self.phone.isValid();
    });

    self.set = function (orderData) {
        self.name(orderData.name || "");
        self.phone(orderData.phone || "");
        self.email(orderData.email || "");
        self.code(orderData.code || "");
        self.contact(orderData.contact || "");
        self.address(orderData.address || "");

        var payment_type_data = orderData.payment_type || {id: 0};
        var payment_type = find(parent.cartChoices.payment_types, function (iter_pt) {
            return iter_pt.id == payment_type_data.id;
        }) || parent.cartChoices.payment_types[0];

        self.payment_type(payment_type);
        self.comment(orderData.comment || "");
    };

    self.set(order);
}

function CartViewModel(config) {
    var self = this;

    var cartDialog = $(".js-cart");

    self.cartItemRemove = function (item) {
        self.cart.remove(item);
    };

    self.cartItemAdd = function (item) {
        if (typeof item != "undefined") {
            var found = find(self.cart(), function (iterItem) {
                return iterItem.id == item.id;
            });
            if (typeof found == "undefined") {
                self.cart.push(item);
            }
        }
    };

    self.cartShow = function () {
        cartDialog.dialog({width: "870px", modal: true, close: self.cartPost});
    };

    self.cartAdd = function () {
        self.cartItemAdd(self.cartCurrentItem);
    };

    self.cartPost = function () {
        $.ajax(config.cartUrl, {
            type: 'POST',
            data: JSON.stringify({
                cart: ko.toJS(self.cart),
                order: ko.toJS(self.order)
            }),
            error: function () {
                $(".js-order-error-message").dialog({
                    modal: true,
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                        }
                    }
                });
            }
        });
    };

    self.showLoginDialog = function () {
        $(".js-login").dialog({
            modal: true,
            width: 780
        });
    };

    self.showLogoutDialog = function () {
        $(".js-logout").dialog({
            modal: true,
            width: 750
        });
    };

    self.closeLoginDialog = function () {
        $(".js-login").dialog("close");
    };

    self.closeLogoutDialog = function () {
        $(".js-logout").dialog("close");
    };

    self.customerLogin = function () {
        if (!self.enableLogin()) {
            return;
        }
        $.ajax(config.customerLoginUrl, {
            type: 'POST',
            data: JSON.stringify({
                login: self.customerLoginName(),
                password: self.customerPassword()
            }),
            success: function (data) {
                self.isAuthenticated(true);
                self.customerName(data.order.name);
                self.order.set(data.order);
                self.closeLoginDialog();
            },
            error: function () {
                $(".js-system-error-message").dialog({
                    modal: true,
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                        }
                    }
                });
            }
        });
    };

    self.customerLogout = function () {
        $.ajax(config.customerLogoutUrl, {
            type: 'POST',
            success: function () {
                window.location.reload(true);
                self.isAuthenticated(false);
                self.customerRegistration("");
                self.customerLoginName("");
                self.customerPassword("");
                self.order.set({});
                self.cartStatus("");
                self.closeLogoutDialog();
            },
            error: function () {
                $(".js-system-error-message").dialog({
                    modal: true,
                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                        }
                    }
                });
            }
        });
    };

    self.cartContinueShopping = function () {
        cartDialog.dialog("close");
        self.cartStatus("");
    };

    self.cartOrder = function () {
        if (!self.cartEnableOrder()) {
            return;
        }
        $.ajax(config.orderUrl, {
            type: 'POST',
            data: JSON.stringify({
                cart: ko.toJS(self.cart),
                password: self.customerPassword(),
                order: ko.toJS(self.order)
            }),
            success: function (data) {
                window.location.href = data;
            },
            error: function (jqXHR) {
                if (jqXHR.status == 403) {
                    self.cartStatus(jqXHR.responseText);
                } else {
                    $(".js-cart-error-message").dialog({
                        modal: true,
                        buttons: {
                            Ok: function () {
                                $(this).dialog("close");
                            }
                        }
                    });
                }
            }
        });
    };

    self.cartItemsFromJs = function (data) {
        var cartItems = [];
        $.each(data, function (idx, product) {
            return cartItems.push(new CartItem(self, product))
        });
        return cartItems;
    };

    self.cartChoices = config.cartChoices;

    self.cart = ko.observableArray(self.cartItemsFromJs(config.cartData.cart));
    if (typeof config.product != "undefined") {
        self.cartCurrentItem = find(self.cart(), function (iterItem) {
            return iterItem.id == config.product.id;
        });
        if (typeof self.cartCurrentItem == "undefined") {
            self.cartCurrentItem = new CartItem(self, config.product);
        }
    }

    self.isAuthenticated = ko.observable(config.isAuthenticated);

    self.customerName = ko.observable(config.customerName);
    self.customerRegistration = ko.observable("");
    self.customerLoginName = ko.observable("").extend({validate: requiredValidator()});
    self.customerPassword = ko.observable("").extend({validate: requiredValidator()});
    self.order = new CartOrder(self, config.cartData.order);

    self.cartStatus = ko.observable("");

    self.cartTotalQuantity = ko.computed(function () {
        return calcSum(self.cart(), function (item) {
            return item.quantity();
        });
    });

    self.cartTotalPriceEur = ko.computed(function () {
        return calcSum(self.cart(), function (item) {
            return item.price_eur * item.quantity();
        });
    });

    self.cartTotalPriceUah = ko.computed(function () {
        return calcSum(self.cart(), function (item) {
            return item.price_uah * item.quantity();
        });
    });

    self.cartShowLogin = ko.computed(function () {
        return !self.isAuthenticated() && self.customerRegistration() == 'login';
    });

    self.cartShowOrder = ko.computed(function () {
        return self.isAuthenticated() || self.customerRegistration() == 'register' || self.customerRegistration() == 'skip';
    });

    self.cartNotEmpty = ko.computed(function () {
        return self.cartTotalQuantity() > 0;
    });

    self.cartEnableOrder = ko.computed(function () {
        return self.cartShowOrder() && self.order.isValid() && self.cartNotEmpty();
    });

    self.enableLogin = ko.computed(function () {
        return self.customerLoginName.isValid() && self.customerPassword.isValid();
    });
}


/* DJANGO CSRF
 ----------------------------------------------------------*/

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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
