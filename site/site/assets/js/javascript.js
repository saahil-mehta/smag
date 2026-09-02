"use strict";

var body = $('body');
var swiper = new Swiper('.page-swiper', {
  slidesPerView: 'auto',
  spaceBetween: 15,
  loop: true,
  centeredSlides: true,
  speed: 600,
  breakpoints: {
    1024: {
      spaceBetween: 30
    }
  },
  navigation: {
    nextEl: '.swiper-next',
    prevEl: '.swiper-prev'
  }
});
var simplePaginationSwiper = new Swiper('.pagination-swiper-container', {
  loop: true,
  autoplay: {
    delay: 6000
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  }
});
var simplePaginationManualSwiper = new Swiper('.pagination-swiper-manual-container', {
  loop: true,
  autoplay: false,
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  }
});
var simpleArrowSwiper = new Swiper('.arrow-swiper-container', {
  loop: true,
  autoHeight: true,
  navigation: {
    nextEl: '.swiper-next',
    prevEl: '.swiper-prev'
  }
});
var gallerySwiper = new Swiper('.gallery-swiper-container', {
  loop: true,
  navigation: {
    nextEl: '.next',
    prevEl: '.prev'
  },
  on: {
    slideChange: function slideChange() {
      $('.product__thumbnails a.active').removeClass('active');
      $('.product__thumbnails a[data-img="' + (this.realIndex + 1) + '"]').addClass('active');
    }
  }
});
$(document).ready(function () {
  $('.InputfieldCheckbox input[type="checkbox"].required').prop('required', true);
  $('select.required, input[type="file"].required').prop('required', 'true');
});
var isTouchDevice = 'ontouchstart' in window || 'onmsgesturechange' in window;
$(function () {
  $('.category-search select').niceSelect();
  if (!isTouchDevice) {
    $('.expandHint').each(function () {
      var text = $('.expandHint__text', this);
      var currentHeight = text.outerHeight();
      var newHeight = currentHeight + $('.expandHint__hidden', this).outerHeight() + 20;
      text.css('height', currentHeight);
      $(this).hover(function () {
        text.css('height', newHeight);
      }, function () {
        text.css('height', currentHeight);
      });
    });
  }
  $('.product__thumbnails a').click(function (e) {
    e.preventDefault();
    if (!$(this).hasClass('active')) {
      var target = $(this).attr('data-img');
      gallerySwiper.slideTo(target);
    }
  });
  $('.accordion__control').click(function () {
    $(this).parent().toggleClass('active');
    $(this).next('.accordion__content').slideToggle(200);
  });
  $('.tabbed-content__tabs a').click(function (e) {
    e.preventDefault();
    $('.tabbed-content__tabs li.active').removeClass('active');
    $(this).parent('li').addClass('active');
    var target = $(this).attr('data-target');
    $('.tab-item').hide();
    $('.tab-item#' + target).show();
  });
  $(".subnav .internal").click(function (e) {
    e.preventDefault();
    var target = $(this).attr('href').substring($(this).attr('href').indexOf('#'));
    $([document.documentElement, document.body]).animate({
      scrollTop: $(target).offset().top
    }, 500);
  });
  if ($(window).width() < 768) {
    $('.responsive-video source').each(function () {
      var targetSrc = 'src',
        videoEl = $(this).parent('video').get(0);
      if ($(this).attr('data-src')) {
        targetSrc = 'data-src';
      }
      if ($(this).attr('data-src-sd')) {
        $(this).attr(targetSrc, $(this).attr('data-src-sd'));
      }
      if (!$(this).parent('video').hasClass('lazy')) {
        videoEl.load();
        videoEl.play();
      }
    });
  }
  var searchUrl = $('#searchfield').attr('data-target');
  $('.js-typeahead').typeahead({
    input: '#site-search',
    order: "asc",
    hint: true,
    display: ['title', 'sku', 'search_tags', 'model_skus'],
    template: "{{title}}",
    templateValue: "{{title}}",
    cancelButton: false,
    href: '{{url}}',
    maxItem: 0,
    generateOnLoad: true,
    correlativeTemplate: true,
    emptyTemplate: "No results found for {{query}} - please try again",
    source: {
      url: searchUrl
    }
  });
  body.on('click', '.burger', function (e) {
    e.preventDefault();
    body.toggleClass('mobile-menu-active');
    $('.mobile-drawer').slideToggle();
  });
  body.on('click', '.expand-search', function (e) {
    e.preventDefault();
    $('.search').addClass('active');
    $('.js-typeahead').focus();
  });
  $('.search .close').click(function (e) {
    e.preventDefault();
    $('.js-typeahead').val('');
    $('.search').removeClass('active');
  });
  $('.mobile-drawer .child-expander').click(function (e) {
    e.preventDefault();
    $(this).parent('.parent').toggleClass('mobile-active');
    $(this).next('.children').slideToggle();
  });
  body.on('click', '.child-expander', function (e) {
    e.preventDefault();
  });
  $('.category-search__filters').on('change', function () {
    $('.grid--product-category').addClass('loading');
    $("select").each(function (index, obj) {
      if ($(obj).val() == "") {
        $(obj).remove();
      }
    });
    document.forms['filterForm'].submit();
  });
  $('input.category-filter').on('change', function (e) {
    e.preventDefault();
    var target = $(this).attr('data-target');
    var joinedValues = $('input[data-target="' + target + '"]:checkbox:checked').map(function () {
      return this.value;
    }).get().join('-');
    $('input[name="' + target + '"]').val(joinedValues);
    $('.filtered-category .category').addClass('loading');
    $('form.filters').submit();
  });
  $('.product-zoom').each(function () {
    var url = $(this).attr('data-zoom');
    $(this).zoom({
      url: url,
      target: $(this).parent('.product__image')
    });
  });
  $('header, .subnav').clone().appendTo('.sticky-header');
  $('input[type="radio"]').parent('label').addClass('radio-label');
  $('input[type="checkbox"]:not(".category-filter")').parent('label').addClass('checkbox-label');
  $('input[type="radio"],input[type="checkbox"]').change(function () {
    inputMarkParent();
  });
  inputMarkParent();
  if ($("#Inputfield_register_confirm").val() && $("#Inputfield_register_email").val()) {
    $('.ConfirmForm').addClass('loading');
    $("#Inputfield_confirm_submit").click();
    setTimeout(function () {
      $('.ConfirmForm').removeClass('loading');
    }, 5000);
  }
});
$(window).scroll(function () {
  if ($(document).scrollTop() > 500) {
    $('.sticky-header').fadeIn(250);
  } else if ($(document).scrollTop() < 1) {
    $('.sticky-header').fadeOut(100);
  }
});
var inputMarkParent = function inputMarkParent() {
  $('input[type="checkbox"], input[type="radio"]').each(function () {
    $(this).parent('label').toggleClass('checked', $(this).prop('checked'));
  });
};
if (document.cookie.indexOf('locationBannerClosed=true') < 0) {
  $('.location-notification').removeClass('pre-check');
  window.scrollTo(0, 0);
}
$('.location-notification__close').click(function () {
  var banner = $('.location-notification');
  banner.css('marginTop', '-' + banner.outerHeight() + 'px');
  document.cookie = "locationBannerClosed=true; path=/;";
});
$('.c2a .button[href*="#webinar"]').each(function () {
  $(this).attr('data-scroll-to', '');
});

// Scroll to
$('[data-scroll-to]').click(function (e) {
  e.preventDefault();
  $('html, body').animate({
    scrollTop: $($(this).attr('href')).offset().top - 100
  }, 500);
  if (this.href.indexOf('#webinar') !== 1) {
    setTimeout(function () {
      $('.show-form-popup').click();
    }, 1200);
  }
});

// Data attr modal video
var modalButtons = $('[data-video-popup]');
if (modalButtons) {
  var _showModal = function _showModal(src) {
    var modal = $('.modal'),
      iframe = $('iframe', modal),
      close = $('.close', modal);
    iframe.attr('src', 'https://www.youtube.com/embed/' + src + '?enablejsapi=1').attr('tabindex', '');
    close.attr('tabindex', '');
    modal.addClass('-open');
    close.click(function () {
      iframe.attr('src', '').attr('tabindex', '-1');
      iframe.attr('tabindex', '-1');
      modal.removeClass('-open');
      $('[data-video-popup][aria-expanded="true"]').attr('aria-expanded', false);
      // Restore the scroll position captured when the modal opened
      var scrollY = parseInt($('body').css('top'), 10) || 0;
      $('body').removeClass('modal-open').css('top', '');
      window.scrollTo(0, -scrollY);
      if (sessionStorage.getItem("data-capture-" + video_id)) {
        sessionStorage.setItem("data-capture-" + video_id, 2);
      }
    });
  };
  var video_id = $('[data-video-popup]').attr('data-video-popup');
  $(document).ready(function () {
    if (sessionStorage.getItem('data-capture-' + video_id) == 1) {
      $('[data-video-popup]').click();
    }
  });
  $('[data-video-popup]').click(function (e) {
    if ($(this).hasClass('show-form-popup') && !sessionStorage.getItem('data-capture-' + video_id)) {
      return;
    }
    e.preventDefault();
    $(this).attr('aria-expanded', true);
    _showModal($(this).attr('data-video-popup'));
    // Preserve scroll position: position:fixed on body would otherwise jump the page to the top
    var scrollY = window.scrollY;
    $('body').css('top', -scrollY + 'px').addClass('modal-open');
  });
}

// popup form modal
var formPopupInit = $('.show-form-popup');
if (formPopupInit) {
  var showFormPopup = function showFormPopup(title, video_id) {
    var popup = $('.popup--form'),
      submit = $('.InputfieldSubmit button', popup),
      close = $('.close', popup),
      inputs = $('.Inputfields input[type!=checkbox]', popup),
      checkbox = $('.Inputfields input[type=checkbox]', popup),
      titleSpan = $('.popup-form__content-title', popup);
    titleSpan.text(title);
    close.attr('tabindex', '');
    popup.addClass('-open');
    close.click(function () {
      popup.removeClass('-open');
      $('.show-form-popup[aria-expanded="true"]').attr('aria-expanded', false);
      $('body').removeClass('popup-open');
    });
    submit.click(function () {
      var inputsValid = true;
      inputs.each(function () {
        if (typeof this.value == 'undefined' || this.value == '') {
          inputsValid = false;
        }
      });
      if (checkbox.prop('checked') && inputsValid) {
        sessionStorage.setItem("data-capture-" + video_id, 1);
        showModal($(this).attr('data-video-popup'));
      }
    });
  };
  $('.show-form-popup').click(function (e) {
    var video_id = $('[data-video-popup]').attr('data-video-popup');
    if (sessionStorage.getItem('data-capture-' + video_id)) {
      return;
    }
    e.preventDefault();
    $(this).attr('aria-expanded', true);
    var title = $(this).find('.title').text();
    showFormPopup(title, video_id);
    $('body').addClass('popup-open');
  });
}

// popup locale modal
var locationPopup = document.querySelector('.popup--location');
if (locationPopup !== null && document.cookie.indexOf('localeSet=') == -1) {
  var showLocationPopup = function showLocationPopup() {
    setTimeout(function () {
      var popup = $('.popup--location'),
        close = $('.close, .cancel', popup);
      close.attr('tabindex', '');
      popup.addClass('-open');
      $('body').addClass('popup-open');
      close.click(function () {
        popup.removeClass('-open');
        $('.show-form-popup[aria-expanded="true"]').attr('aria-expanded', false);
        $('body').removeClass('popup-open');
        document.cookie = "localeSet=true;path=/;expires=86400;";
      });
    }, 5000);
  };
  showLocationPopup();
}
function showPromoPopup() {
  if (document.cookie.indexOf('promoClose=') == -1) {
    setTimeout(function () {
      var popup = $('.popup--promo'),
        close = $('.close', popup);
      close.attr('tabindex', '');
      popup.addClass('-open');
      close.click(function () {
        popup.removeClass('-open');
        $('.show-form-popup[aria-expanded="true"]').attr('aria-expanded', false);
        $('body').removeClass('popup-open');
        document.cookie = "promoClose=true;path=/;expires=86400;";
      });
    }, 8000);
  }
}
showPromoPopup();